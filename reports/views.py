from django.views import generic
from .mixins import ShowOwnerReportsListMixin, ShowGuestReportsListMixin
from .forms import MailboxValidateForm


class ReportListView(ShowOwnerReportsListMixin, ShowGuestReportsListMixin, generic.TemplateView):
    template_name = 'reports/report_list_template.html'


class MailboxValidateView(generic.FormView):
    template_name = 'mailboxes/mailbox_validate_template.html'
    form_class = MailboxValidateForm


class ReportCreateView(generic.TemplateView):
    template_name = 'reports/report_create_template.html'
