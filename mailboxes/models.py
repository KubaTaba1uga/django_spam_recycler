from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
"""Required for importing custom user model
"""


class MailboxModel(models.Model):
    email_address = models.CharField(max_length=32)
    """App use `email_address` to connect to email server
    """
    server_address = models.CharField(max_length=255)
    """App use `email_server_address` as IMAP connection endpoint
    """
    owner = models.ForeignKey(
        get_user_model(),
        #  Tell Django to use `CustomUser` as foreign key
        on_delete=models.CASCADE, related_name="owned_mailbox")
    """User which owns `MailboxModel` instance
    """

    guests = models.ManyToManyField(
        get_user_model(),
        through='MailboxGuestModel', related_name="guest_mailbox")

    def get_absolute_url(self):
        return reverse("mailboxes:mailbox_details_url", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.email_address

    class Meta:
        unique_together = ('email_address', 'owner', 'server_address')


class MailboxGuestModel(models.Model):
    mailbox = models.ForeignKey(
        MailboxModel,
        on_delete=models.CASCADE,
        related_name='guest_mailbox'
    )
    guest = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name='mailbox_guest'
    )
    """ User with read-only permissions to `MailboxModel`
    """

    def __str__(self) -> str:
        return f"{self.mailbox}+{self.guest}"

    class Meta:

        """ Each user can be guest to multiple mailboxes as it is not repetion
        """
        unique_together = ('guest', 'mailbox')
