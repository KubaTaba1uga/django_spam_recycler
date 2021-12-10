from shared_code.name_utils import (
    create_user_spam_queue_name,
     create_user_email_queue_name,
     create_worker_celery_name)
from subprocess import Popen, PIPE

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
