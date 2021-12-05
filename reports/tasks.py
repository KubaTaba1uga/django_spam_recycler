import asyncio
import logging
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from shared_code.aiospamc_utils import create_report
from shared_code.queries import get_report_by_id_and_owner, create_message_evaluation
from shared_code.queries import create_message as save_message_to_db
from shared_code.worker_utils import create_user_email_queue, create_user_spam_queue
from shared_code.imap_sync import create_search_from_str, gather_emails_GUIDs, download_message_by_guid, parse_message
from shared_code.name_utils import create_user_spam_queue_name
from .models import MessageModel


"""
    Shedule periodic task to check if user has reports to generate
    If not kill user spam and email workers

    Run every 5 minutes

    Kill workers if:
        1. Spam queue is empty
        2. Email queue is empty
        3. There are no new generate report tasks for user
"""

retry_policy = {'max_retries': 30,
                'interval_start': 5,
                'interval_step': 5,
                }


@shared_task(bind=True)
def download_email_task(
        self, email_guid, mailbox_credentials, folder, report_id):
    try:
        message = download_message_by_guid(
            mailbox_credentials,
            guid=email_guid)

        message = parse_message(message)

    except Exception as e:
        """ Because of hard to predict errors in imap-tools, retry on every Exception
        """
        logging.error(e)
        raise self.retry(exc=e)

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
                queue=email_queue,
                retry=True,
                retry_policy=retry_policy)

            report.messages_counter += 1

    report.save()

    return "Report for user {} has been generated".format(user_id)


@shared_task
def evaluate_message_spam(message, message_id):
    report = asyncio.run(create_report(message.encode('utf-8')))

    message_evaluation = create_message_evaluation(
        report['spam_score'],
        report['spam_description'],
     message_id)

    return "Spam evaluation for message {} has been created".format(message_id)


@receiver(post_save, sender=MessageModel)
def queue_task(sender, instance, created, **kwargs):
    """ Evaluate message spam when message is saved to db
    """
    spam_queue = create_user_spam_queue_name(instance.report.mailbox.owner.id)

    message = str(instance.orginal_message)

    evaluate_message_spam.apply_async(
        args=[message, int(instance.id)],
        queue=spam_queue, retry=True,
                retry_policy=retry_policy)
