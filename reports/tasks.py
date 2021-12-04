from random import randint
from socket import gaierror
from celery import shared_task, Task
from shared_code.worker_utils import create_user_email_queue, create_user_spam_queue

"""
    Shedule periodic task to check if user has reports to generate
    If not kill user spam and email workers

    Run every 5 minutes

    Kill workers if:
        1. Spam queue is empty
        2. Email queue is empty
        3. There are no new generate report tasks for user
"""


class BaseTaskWithRetry(Task):
    autoretry_for = (gaierror, ValueError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = randint(1, 90)
    retry_jitter = True


@shared_task
def generate_report_task(
        user_id, folder_list, email_address, server_address, password):
    """
    Generate spam evaluation report for user with user_id
    :param user_id:
    :return:
    """

    create_user_email_queue(user_id)
    create_user_spam_queue(user_id)

    return "Report for user {} has been generated".format(user_id)
