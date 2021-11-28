from django.db import models
from mailboxes.models import MailboxModel


class ReportModel(models.Model):
    name = models.CharField(max_length=32)
    overall = models.IntegerField(default=0)
    """ Score that indicate, mailbox spam vulnerability
    """
    mailbox = models.ForeignKey(
        MailboxModel,
        on_delete=models.CASCADE,
     related_name='report')
    """ Mailbox to which report relate to
    """
    created_at = models.DateTimeField(auto_now_add=True)
    """ When report was generated
    """
    start_at = models.DateTimeField()
    """ When search start
    """
    end_at = models.DateTimeField()
    """ When search end
    """
    messages_counter = models.IntegerField()
    """ How many messages to report
    """

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'mailbox')


class MessageModel(models.Model):
    subject = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    to_recipients = models.CharField(max_length=255)
    received_at = models.DateTimeField()
    body = models.TextField()
    folder = models.CharField(max_length=255)
    report = models.ForeignKey(ReportModel,
                               on_delete=models.CASCADE,
                               related_name='messages')

    def __str__(self):
        return self.subject


class MessageEvaluationModel(models.Model):
    spam_score = models.IntegerField()
    """ Indicate email spam potential
    """
    spam_description = models.TextField()
    """ Spam score explanation
    """
    message = models.OneToOneField(
        MessageModel,
        models.CASCADE,
     related_name='spam_evaluation')

    def __str__(self):
        return f'{self.message.subject} {self.spam_score}'
