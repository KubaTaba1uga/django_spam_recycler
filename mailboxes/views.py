from django.views import generic
from .models import MailboxModel
from .mixins import ShowMailboxGuestMixin, ShowMailboxOwnerMixin


class MailboxListView(ShowMailboxGuestMixin, ShowMailboxOwnerMixin, generic.ListView):
    template_name = 'mailboxes/mailbox_list_template.html'
    model = MailboxModel
    context_object_name = 'mailboxes'
