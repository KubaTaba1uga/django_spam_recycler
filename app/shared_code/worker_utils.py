from subprocess import Popen, PIPE
from django.contrib.auth import get_user_model
from celery import shared_task
from config.celery import app
from shared_code.name_utils import (
    create_user_spam_queue_name,
    create_user_email_queue_name,
    create_worker_celery_name,
    create_spam_worker_celery_name,
    create_email_worker_celery_name
)


SCRIPT_PATH = '/code/scripts/set_up_user_queues.py'

COMMAND_EXEC = 'python'

MAIN_WORKER_NAME = create_worker_celery_name('main_worker')


def execute_command(command):
    process = Popen(command.split(), stdout=PIPE)
    if process.wait() != 0:
        print(process.stdout.read())
        raise Exception(f'Error executing command: {command}')


def create_user_spam_queue(user_id):
    """
    Create a queue for each user
    """
    queue_name = create_user_spam_queue_name(user_id)
    execute_command(f'{COMMAND_EXEC} {SCRIPT_PATH} {user_id} spam')
    return queue_name


def create_user_email_queue(user_id):
    """
    Create a queue for each user
    """
    queue_name = create_user_email_queue_name(user_id)
    execute_command(f'{COMMAND_EXEC} {SCRIPT_PATH} {user_id} email')
    return queue_name


@shared_task
def delete_workers():
        """
        Shedule periodic task to check if user has reports to generate
        If not kill user spam and email workers

        Run every 10 minutes

        Kill workers if:
            1. Spam queue is empty
            2. Email queue is empty
            3. There are no new generate report tasks for user
        """

        main_inspect = app.control.inspect([MAIN_WORKER_NAME])

        for user in get_user_model().objects.all():
            spam_worker_name = create_spam_worker_celery_name(user.id)

            email_worker_name = create_email_worker_celery_name(user.id)

            spam_inspect = app.control.inspect([spam_worker_name])

            email_inspect = app.control.inspect([email_worker_name])

            main_tasks = main_inspect.active().get(
                MAIN_WORKER_NAME) + main_inspect.reserved().get(MAIN_WORKER_NAME)

            if main_tasks:
                """ If main queue is proceeding any user task, skip workers deleting
                """
                is_proceeding = False

                for task in main_tasks:
                    if len(task['args']) > 0:
                        if task['args'][0] == user.id:
                            is_proceeding = True
                        break

                if is_proceeding:
                    continue

            if not spam_inspect.ping() or not email_inspect.ping():
                """ If workers are not found, skip workers deleting
                """
                continue

            if spam_inspect.active().get(spam_worker_name):
                """ If user spam queue is proceeding any task, skip workers deleting
                """
                continue

            if spam_inspect.reserved().get(spam_worker_name):
                """ If user spam queue is not empty, skip workers deleting
                """
                continue

            if email_inspect.active().get(email_worker_name):
                """ If user email queue is proceeding any task, skip workers deleting
                """
                continue

            if email_inspect.reserved().get(email_worker_name):
                """ If user email queue is not empty, skip workers deleting
                """
                continue

            app.control.broadcast(
                'shutdown',
                destination=[
                    spam_worker_name,
                    email_worker_name])
