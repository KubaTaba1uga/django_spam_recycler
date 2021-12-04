from random import randint
from socket import gaierror
from celery import shared_task, Task
from shared_code.queries import create_report
from shared_code.queries import create_message as save_message_to_db
from shared_code.worker_utils import create_user_email_queue, create_user_spam_queue
from shared_code.imap_sync import create_search_from_str, gather_emails_GUIDs, download_message_by_guid
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


def create_email(message):
    return {
        'subject': message.subject,
        'sender': message.from_values.email,
        'to_recipients': " ,".join(to.email for to in message.to_values),
        'received_at': message.date,
        'body': message.html
    }


@shared_task(base=BaseTaskWithRetry)
def download_email_task(email_guid, mailbox_credentials, folder, report_id):

    message = download_message_by_guid(mailbox_credentials, guid=email_guid)

    message = create_email(message)

    save_message_to_db(
        message['subject'],
        message['sender'],
        message['to_recipients'],
        message['received_at'],
        message['body'],
        folder,
        report_id
    )


@shared_task
def generate_report_task(
        user_id, folder_list, start_date, end_date, mailbox_credentials, report_name, mailbox_id):
    """
    Generate spam evaluation report for user with user_id

    Set up worker and queue for email downloading
    Set up worker and queue for spam evaluation


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

    search = create_search_from_str(start_date, end_date)

    report = create_report(
        name=report_name,
        start_at=start_date,
        end_at=end_date,
        mailbox_id=mailbox_id)

    for folder in folder_list:
        for email_guid in gather_emails_GUIDs(mailbox_credentials=mailbox_credentials, folder=folder, search=search):
            download_email_task.apply_async(
                args=[email_guid,
                      mailbox_credentials, folder, report.id],
                queue=email_queue)

    return "Report for user {} has been generated".format(user_id)
