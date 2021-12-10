from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from mailboxes.forms import PasswordForm
from mailboxes.models import MailboxModel
from shared_code.queries import get_user_owner_mailboxes_tuples
from .models import ReportModel


class MailboxValidateForm(PasswordForm):

    """
    Validate mailbox by IMAP
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['email_address'] = forms.ChoiceField(
            choices=get_user_owner_mailboxes_tuples(self.user), required=True)

    def form_valid(self, form):

        return super().form_valid(form)

    class Meta:
        model = MailboxModel
        exclude = ['owner', 'guests', 'server_address']


class ReportGenerateForm(forms.ModelForm):

    def is_valid(self, user) -> bool:
        if super().is_valid():
            form = {
                field.name: field.value()
                for field in self.visible_fields()
            }

            if form.get('start_at') < form.get('end_at'):
                return True

        self.add_error(
            'start_at',
            f'`Start at` field cannot be later than `End at` field')

        return False

    class Meta:
        model = ReportModel
        exclude = ['owner', 'mailbox', 'overall', 'messages_counter']
        widgets = {
            'start_at': AdminDateWidget(attrs={'type': 'date'}),
            'end_at': AdminDateWidget(attrs={'type': 'date'}),
        }
