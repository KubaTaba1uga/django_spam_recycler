from shared_code.queries import get_user_owner_mailboxes_query
from .models import MailboxModel, MailboxGuestModel
from django import forms


class PasswordForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class MailboxCreateForm(PasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].widget = forms.HiddenInput()

    class Meta:
        model = MailboxModel
        exclude = ['guests']


class MailboxUpdateForm(PasswordForm):

    class Meta:
        model = MailboxModel
        exclude = ['owner', 'guests']


class MailboxAddGuestForm(forms.ModelForm):

    """ Only owners can add guests
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields[
            'mailbox'].queryset = get_user_owner_mailboxes_query(self.user)

    class Meta:
        model = MailboxGuestModel
        exclude = ['owner', 'server_address']
