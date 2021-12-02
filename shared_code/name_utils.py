def create_worker_name(user_id):
    return f'user_{user_id}_celery_worker'


def create_worker_celery_name(worker_name):
    return f"celery@{worker_name}"


def create_user_spam_queue_name(user_id):
    return f'user_{user_id}_spam_queue'
