from .models import MailboxModel
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
