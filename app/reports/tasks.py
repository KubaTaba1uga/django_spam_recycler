import asyncio
from imap_tools.errors import MailboxLoginError
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from config.celery import app
from shared_code.aiospamc_utils import create_report
from shared_code.queries import get_report_by_id, get_report_by_id_and_owner, create_message_evaluation
from shared_code.queries import create_message as save_message_to_db
from shared_code.worker_utils import create_user_email_queue, create_user_spam_queue, delete_workers
from shared_code.imap_sync import create_search_from_str, gather_emails_GUIDs, download_message_by_guid, parse_message
from shared_code.name_utils import create_user_spam_queue_name
from .models import MessageModel

# Task will retry as long as it fails
#  because at this point all data are already validated


@shared_task(bind=True, default_retry_delay=5, max_retries=None)
def download_email_task(
        self, email_guid, mailbox_credentials, folder, report_id):

    try:
        message = download_message_by_guid(
            mailbox_credentials,
            guid=email_guid)

    except MailboxLoginError:
        # Error thrown by imap_tools in case of collision
        #   when multiple apps try to login to the same mailbox.
        #   Even if credentials are correct
        #   imap.gmail.com return "NO" in place of "OK"

        self.retry()

    if not message:
        # imap_tools.mailbox.fetch sometimes
        #  return None in place of Message object

        self.retry()

    else:

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


@shared_task
def evaluate_message_spam(message, message_id):
    report = asyncio.run(create_report(message.encode('utf-8')))

    create_message_evaluation(
        report['spam_score'],
        report['spam_description'],
     message_id)

    return "Spam evaluation for message {} has been created".format(message_id)


@receiver(post_save, sender=MessageModel)
def queue_task(sender, instance, created, **kwargs):
    """ Evaluate message spam capability
         when message is saved to db
    """
    user_id = instance.report.mailbox.owner.id

    spam_queue = create_user_spam_queue_name(user_id)

    message = str(instance.orginal_message)

    evaluate_message_spam.apply_async(
        args=[message, int(instance.id)],
        queue=spam_queue)


app.task(delete_workers)
# Include task from shared_code.worker_utils.delete_workers
#   as dynamic workers deleting is used, upon report creation
