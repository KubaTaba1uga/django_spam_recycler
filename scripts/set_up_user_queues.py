import sys
from subprocess import Popen, PIPE, CalledProcessError
import json

PIDFILES_FOLDER = '/home/taba1uga/celery_workers/'
""" Store pidfiles on disk to avoid multiple
        workers for the same user
"""


def unpack_json(json_string):
    try:
        output = json.loads(json_string)
    except json.decoder.JSONDecodeError:
        output = {}
    return output


def create_worker_name(user_id):
    return f'user_{user_id}_celery_worker'


def create_worker_celery_name(worker_name):
    return f"celery@{worker_name}"


def create_user_spam_queue(user_id):
    return f'user_{user_id}_spam_queue'


def execute_command(command):
    return Popen(command.split(), stdout=PIPE)


def get_worker_queues(worker_name):
    """
    Returns the queues of a worker
    """
    worker_name = f'celery@{worker_name}'
    COMMAND = f'celery -A config inspect active_queues -d {worker_name} -j'

    queues = execute_command(COMMAND)
    queues = unpack_json(queues.stdout.read())

    if queues:
        return queues[worker_name]
    else:
        return {}


def does_worker_exist(worker_name):
    """
    Checks if a worker exists on the celery
    """
    COMMAND = 'celery -A config inspect registered -j'

    try:
        with execute_command(COMMAND) as process:
            for worker in unpack_json(process.stdout.read()):
                if worker == worker_name:
                    return True
        return False

    except CalledProcessError:
        return False


def create_worker(worker_name):
    """
    Creates a worker on the celery
    """

    COMMAND = f'celery -A config worker -n {worker_name} -c 1 --detach --pidfile {PIDFILES_FOLDER}{worker_name}.pid'

    worker_creation = execute_command(COMMAND)

    if worker_creation.wait() != 0:
        raise CalledProcessError


def unconsume_queue_by_worker(worker_name, queue_name):
    """
    Unconsume a queue by a worker
    """

    COMMAND = f'celery -A config control cancel_consumer {queue_name} -d {worker_name}'

    process = execute_command(COMMAND)
    process.wait()


def consume_queue_by_worker(worker_name, queue_name):
    """
    Consume a queue by a worker
    """

    COMMAND = f'celery -A config control add_consumer {queue_name} -d {worker_name}'

    process = execute_command(COMMAND)
    process.wait()


def main(worker_name, spam_queue_name):
    """
    Create a worker and a queues for each user
        if it doesn't exist

    Queues:
        - spam_queue: queue for evaluating spam score
    """

    worker_celery_name = create_worker_celery_name(worker_name)
    create_worker(worker_name)

    if not does_worker_exist(worker_celery_name):

        main(worker_name, spam_queue_name)

    for queue in get_worker_queues(worker_name):
        """
        Unconsume all queues beside user's spam_queue
        """
        if queue['name'] != spam_queue_name:

            unconsume_queue_by_worker(worker_celery_name, queue['name'])

        else:
            return
    """
    Add spam_queue only if it is not already being consumed
    """
    consume_queue_by_worker(worker_celery_name, spam_queue_name)


if __name__ == '__main__':
    """
    Each user should have a worker and a queue specially for spam evaluation
        the goal is evaluating and downloading spam emails simultaneously
    """
    user_id = sys.argv[1]

    worker_name = create_worker_name(user_id)
    spam_queue_name = create_user_spam_queue(user_id)
    main(worker_name, spam_queue_name)
