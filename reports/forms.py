from mailboxes.forms import MailboxCreateForm
from mailboxes.models import MailboxModel
from django import forms


class MailboxValidateForm(MailboxCreateForm):

    """
    Validate mailbox by IMAP
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['server_address'].widget = forms.HiddenInput()

    class Meta:
        model = MailboxModel
        exclude = ['owner', 'guests']
