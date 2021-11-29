from shared_code.rabbit_mq import create_rabbit_mq_queue_with_worker, is_queue_created


def create_user_download_emails(user_id):
    """
    Create a queue for downloading emails
    """
    download_emails_queue_name = f"user_{user_id}_download_emails"

    print(
        'download_emails_queue',
        is_queue_created(download_emails_queue_name))

    if not is_queue_created(download_emails_queue_name):

        print('Creating queue', download_emails_queue_name)

        create_rabbit_mq_queue_with_worker(download_emails_queue_name)


def create_user_evaluate_spam(user_id):
    """
    Create a queue for evaluating email spam score
    """
    evaluate_spam_score_queue_name = f"user_{user_id}_evaluate_spam_score"

    print(
        'evaluate_spam_score_queue',
        is_queue_created(evaluate_spam_score_queue_name))

    if not is_queue_created(evaluate_spam_score_queue_name):

        print('Creating queue', evaluate_spam_score_queue_name)

        create_rabbit_mq_queue_with_worker(evaluate_spam_score_queue_name)


def create_user_queues(user_id):
    """
    Create a queue for each user
    """
    create_user_download_emails(user_id)
    create_user_evaluate_spam(user_id)
