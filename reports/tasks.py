from random import randint
from socket import gaierror
from celery import shared_task, Task
from shared_code.queries import get_report_by_id_and_owner
from shared_code.queries import create_message as save_message_to_db
from shared_code.worker_utils import create_user_email_queue, create_user_spam_queue
from shared_code.imap_sync import create_search_from_str, gather_emails_GUIDs, download_message_by_guid, parse_message
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


@shared_task(base=BaseTaskWithRetry)
def download_email_task(email_guid, mailbox_credentials, folder, report_id):

    message = download_message_by_guid(mailbox_credentials, guid=email_guid)

    message = parse_message(message)

    save_message_to_db(
        message['subject'],
        message['sender'],
        message['to_recipients'],
        message['received_at'],
        message['body'],
        message['orginal_message'],
        folder,
        report_id,
    )

    return "Message {} for report {} has been downloaded".format(email_guid, report_id)


@shared_task
def generate_report_task(
        user_id, folder_list, start_date, end_date, mailbox_credentials, report_id):
    """
    Generate spam evaluation report for user with user_id

    Set up worker and queue for email downloading
    Set up worker and queue for spam evaluation

    """

    email_queue = create_user_email_queue(user_id)

    spam_queue = create_user_spam_queue(user_id)

    report = get_report_by_id_and_owner(report_id, user_id)

    search = create_search_from_str(start_date, end_date)

    for folder in folder_list:
        for email_guid in gather_emails_GUIDs(mailbox_credentials=mailbox_credentials, folder=folder, search=search):

            download_email_task.apply_async(
                args=[email_guid,
                      mailbox_credentials, folder, report_id],
                queue=email_queue)

            report.messages_counter += 1

    report.save()

    return "Report for user {} has been generated".format(user_id)
