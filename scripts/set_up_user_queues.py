import sys
import logging
from subprocess import Popen, PIPE, CalledProcessError
import json


def execute_command(command):
    return Popen(command.split(), stdout=PIPE)


def get_worker_queues(worker_name):
    """
    Returns the queues of a worker
    """
    worker_name = f'celery@{worker_name}'
    COMMAND = f'celery -A config inspect active_queues -d {worker_name} -j'

    queues = execute_command(COMMAND)
    queues = queues.stdout.read().decode('utf-8')

    return json.loads(queues)[worker_name]


def does_worker_exist(worker_name):
    """
    Checks if a worker exists on the celery
    """

    try:
        COMMAND = 'celery -A config inspect registered'

        with execute_command(COMMAND) as process:
            to_check = process.stdout.read().decode('utf-8')
            for element in to_check.split():
                if worker_name in element:
                    return True

        return False

    except CalledProcessError:

        return False


def create_worker(worker_name, queue_name):
    """
    Creates a worker on the celery
    """
    try:
        COMMAND = f'celery -A config worker -n {worker_name} -c 1 --detach'

        worker_creation = execute_command(COMMAND)

        if worker_creation.wait() != 0:
            raise CalledProcessError

    except CalledProcessError:
        logging.error(f'Error while creating worker {worker_name}')
        return False


def unconsume_queue_by_worker(worker_name, queue_name):
    """
    Unconsume a queue by a worker
    """

    worker_name = f'celery@{worker_name}'

    COMMAND = f'celery -A config control cancel_consumer {queue_name} -d {worker_name}'

    process = execute_command(COMMAND)
    process.wait()


def consume_queue_by_worker(worker_name, queue_name):
    """
    Consume a queue by a worker
    """

    worker_name = f'celery@{worker_name}'

    COMMAND = f'celery -A config control add_consumer {queue_name} -d {worker_name}'

    process = execute_command(COMMAND)
    process.wait()


def main(worker_name, spam_queue_name):
    """
    Main function
    """
    if not does_worker_exist(worker_name):
        create_worker(worker_name)
        main(worker_name, spam_queue_name)
    else:
        print(f'Worker {worker_name} already exists')

        for queue in get_worker_queues(worker_name):
            """
            Unconsume all queues beside user spam evaluation queue
            """
            if queue['name'] != spam_queue_name:
                unconsume_queue_by_worker(worker_name, queue['name'])
            else:
                print(f'{worker_name} is already consuming {queue["name"]}')
                return
        """
        Add queue only if it is not already being consumed
        """
        consume_queue_by_worker(worker_name, spam_queue_name)


if __name__ == '__main__':
    user_id = sys.argv[1]

    worker_name = f'user_{user_id}_celery_worker'
    spam_queue_name = f"user_{user_id}_spam_queue"

    main(worker_name, spam_queue_name)
