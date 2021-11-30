from shared_code.rabbit_mq import create_detached_worker, is_queue_created
from multiprocessing import Process


def create_user_download_emails(user_id):
    """
    Create a queue for downloading emails
    """
    download_emails_queue_name = f"user_{user_id}_download_emails+4"

    print(
        'download_emails_queue',
        is_queue_created(download_emails_queue_name))

    if not is_queue_created(download_emails_queue_name):

        print('Creating queue', download_emails_queue_name)
        create_detached_worker(download_emails_queue_name)
        start_worker = Process(
            target=create_detached_worker,
            args=(download_emails_queue_name,
                  ))
        # start_worker.setDaemon(True)
        # start_worker.start()


def create_user_evaluate_spam(user_id):
    """
    Create a queue for evaluating email spam score
    """
    evaluate_spam_score_queue_name = f"user_{user_id}_evaluate_spam_score+4"

    print(
        'evaluate_spam_score_queue',
        is_queue_created(evaluate_spam_score_queue_name))

    if not is_queue_created(evaluate_spam_score_queue_name):

        print('Creating queue', evaluate_spam_score_queue_name)

        Process(
            target=create_detached_worker,
            args=(evaluate_spam_score_queue_name,
                  ))  # .start()


def create_user_queues(user_id):
    """
    Create a queue for each user
    """
    # create_detached_worker(user_id)
    # create_detached_worker(user_id)
    create_user_download_emails(user_id)
    create_user_evaluate_spam(user_id)
