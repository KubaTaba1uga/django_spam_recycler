from config.celery import app
from celery.platforms import detached, create_pidlock


def create_detached_worker(queue_name):
    """
    Create a queue with a worker
    """

    with detached(logfile=f'/var/run/celery/{queue_name}.log',
                  pidfile=f'/var/run/celery/{queue_name}.pid',
                  uid='root'):

        create_pidlock(f'/var/run/celery/{queue_name}.pid')

        worker = app.Worker(
            hostname=queue_name,
        )

        app.control.add_consumer(queue_name,
                                 destination=['celery@' + queue_name])

        worker.start()


def generate_queue_list():
    workers = app.control.inspect().active_queues()
    for queues in workers.values():
        for queue in queues:
            yield queue['name']


def is_queue_created(queue_name):
    """
    Check if a queue is created
    """
    for queue in generate_queue_list():
        if queue == queue_name:
            return True
    return False
