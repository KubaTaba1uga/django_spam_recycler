from django.views import generic
from .models import MailboxModel
from .mixins import (
    ShowMailboxGuestMixin,
     ShowMailboxOwnerMixin,
     AddMailboxOwnerMixin,
     ValidateMailboxImapMixin)
from .forms import MailboxCreateForm


class MailboxListView(ShowMailboxGuestMixin, ShowMailboxOwnerMixin, generic.ListView):
    template_name = 'mailboxes/mailbox_list_template.html'
    model = MailboxModel


class MailboxCreateView(AddMailboxOwnerMixin, ValidateMailboxImapMixin, generic.CreateView):

    """ Create mailbox if:
        - email server address is valid
        - email address is valid
        - email address password is valid
    """
    template_name = 'mailboxes/mailbox_create_template.html'
    model = MailboxModel
    form_class = MailboxCreateForm


class MailboxDetailsView(generic.DetailView):
    template_name = 'mailboxes/mailbox_details_template.html'
    model = MailboxModel
    context_object_name = 'mailbox'
