def create_spam_worker_name(user_id):
    return f'user_{user_id}_spam_worker'


def create_email_worker_name(user_id):
    return f'user_{user_id}_email_worker'


def create_worker_celery_name(worker_name):
    return f"celery@{worker_name}"


def create_spam_worker_celery_name(user_id):
    return create_worker_celery_name(create_spam_worker_name(user_id))


def create_email_worker_celery_name(user_id):
    return create_worker_celery_name(create_email_worker_name(user_id))


def create_user_spam_queue_name(user_id):
    return f'user_{user_id}_spam_queue'


def create_user_email_queue_name(user_id):
    return f'user_{user_id}_email_queue'
