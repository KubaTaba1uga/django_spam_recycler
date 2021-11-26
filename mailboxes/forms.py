from .models import MailboxModel
from django import forms


class MailboxCreateForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].widget = forms.HiddenInput()

    class Meta:
        model = MailboxModel
        exclude = ['guests']
