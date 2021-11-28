from django.views import generic
from django.urls import reverse_lazy
from mailboxes.mixins import PassLoggedUserToFormMixin
from .mixins import ShowOwnerReportsListMixin, ShowGuestReportsListMixin, ValidateMailboxImapMixin, ValidateMailboxOwnerMixin
from .forms import MailboxValidateForm


class ReportListView(ShowOwnerReportsListMixin, ShowGuestReportsListMixin, generic.TemplateView):
    template_name = 'reports/report_list_template.html'


class MailboxValidateView(ValidateMailboxOwnerMixin, ValidateMailboxImapMixin, PassLoggedUserToFormMixin, generic.FormView):
    template_name = 'reports/mailbox_validate_template.html'
    form_class = MailboxValidateForm
    success_url = reverse_lazy('reports:report_validate_mailbox_url')


class ReportCreateView(generic.TemplateView):
    template_name = 'reports/report_create_template.html'
