from config.celery import app
import celery


def create_rabbit_mq_queue_with_worker(queue_name):
    """
    Create a queue with a worker
    """
    worker = app.Worker(
        hostname=queue_name
    )
    app.control.add_consumer(queue_name,
                             destination=[queue_name])


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
