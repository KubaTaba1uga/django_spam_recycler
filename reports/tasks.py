from random import randint
from socket import gaierror
from celery import shared_task, Task
from shared_code.worker_utils import create_user_email_queue, create_user_spam_queue
from shared_code.imap_sync import create_mailbox
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


def gather_emails_GUIDs(mailbox, search):
    """ Download GUID of messages passing search requirements
    """
    return (email for email in mailbox.uids(search))


@shared_task
def generate_report_task(
        user_id, folder_list, start_date, end_date, mailbox_credentials):
    """
    Generate spam evaluation report for user with user_id
    :param user_id: int
    :param folder_list: list
    :param start_date: str
    :param end_date: str
    :param email_address: str
    :param server_address: str
    :param password: str
    :return :str
    """

    email_queue = create_user_email_queue(user_id)
    spam_queue = create_user_spam_queue(user_id)

    mailbox = create_mailbox(**mailbox_credentials)

    for email in gather_emails_GUIDs(mailbox, folder_list):
        pass
    return email
    return "Report for user {} has been generated".format(user_id)
