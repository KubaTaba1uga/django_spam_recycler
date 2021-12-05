from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MailboxModel, MailboxGuestModel
from .mixins import (
    ShowGuestMailboxListMixin,
    ShowOwnerMailboxListMixin,
    AddMailboxOwnerMixin,
    ValidateMailboxImapMixin,
    PassLoggedUserToFormMixin,
    MailboxOwnerOnlyMixin,
    MailboxOwnerAndGuestOnlyMixin,
    ShowMailboxGuestsMixin,
    GuestMailboxOwnerOnlyMixin)
from .forms import (
    MailboxCreateForm,
     MailboxUpdateForm,
     MailboxAddGuestForm)


class MailboxListView(LoginRequiredMixin, ShowOwnerMailboxListMixin, ShowGuestMailboxListMixin, generic.TemplateView):
    template_name = 'mailboxes/mailbox_list_template.html'


class MailboxCreateView(LoginRequiredMixin, AddMailboxOwnerMixin, ValidateMailboxImapMixin, generic.CreateView):

    """ Create mailbox, after imap validation suceed
    """
    template_name = 'mailboxes/mailbox_create_template.html'
    model = MailboxModel
    form_class = MailboxCreateForm


class MailboxEditView(LoginRequiredMixin, MailboxOwnerOnlyMixin, ValidateMailboxImapMixin, generic.UpdateView):
    template_name = 'mailboxes/mailbox_edit_template.html'
    model = MailboxModel
    form_class = MailboxUpdateForm


class MailboxDetailsView(LoginRequiredMixin, ShowMailboxGuestsMixin, MailboxOwnerAndGuestOnlyMixin, generic.DetailView):
    template_name = 'mailboxes/mailbox_details_template.html'
    model = MailboxModel
    context_object_name = 'mailbox'


class MailboxDeleteView(LoginRequiredMixin, MailboxOwnerOnlyMixin, generic.DeleteView):
    template_name = 'mailboxes/mailbox_delete_template.html'
    model = MailboxModel
    context_object_name = 'mailbox'
    success_url = reverse_lazy('mailboxes:mailbox_list_url')


class MailboxAddGuestView(LoginRequiredMixin, PassLoggedUserToFormMixin, generic.CreateView):
    template_name = 'mailboxes/mailbox_add_guest_template.html'
    model = MailboxGuestModel
    form_class = MailboxAddGuestForm


class MailboxGuestDeleteView(LoginRequiredMixin, GuestMailboxOwnerOnlyMixin, generic.DeleteView):
    template_name = 'mailboxes/mailbox_delete_guest_template.html'
    model = MailboxGuestModel
    context_object_name = 'mailbox_guest'
    success_url = reverse_lazy('mailboxes:mailbox_list_url')

    def get_success_url(self):
        """ Overwrite success url to redirect to mailbox details view
        """
        return reverse_lazy('mailboxes:mailbox_details_url', kwargs={'pk': self.object.mailbox.pk})
