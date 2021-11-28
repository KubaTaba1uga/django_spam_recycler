from mailboxes.forms import PasswordForm
from mailboxes.models import MailboxModel
from shared_code.queries import get_user_owner_mailboxes_tuples
from django import forms


class MailboxValidateForm(PasswordForm):

    """
    Validate mailbox by IMAP
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['server_address'].widget = forms.HiddenInput()
        self.fields['email_address'] = forms.ChoiceField(
            choices=get_user_owner_mailboxes_tuples(self.user), required=True)

    class Meta:
        model = MailboxModel
        exclude = ['owner', 'guests']
