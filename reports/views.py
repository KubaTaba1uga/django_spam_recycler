from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from mailboxes.mixins import PassLoggedUserToFormMixin
from shared_code.imap_sync import get_mailbox_folder_list
from .mixins import ShowOwnerReportsListMixin, ShowGuestReportsListMixin, ValidateMailboxImapMixin, ValidateMailboxOwnerMixin
from .forms import MailboxValidateForm, ReportGenerateForm


class ReportListView(ShowOwnerReportsListMixin, ShowGuestReportsListMixin, generic.TemplateView):
    template_name = 'reports/report_list_template.html'


class ReportCreateView(generic.View):
    template_name = 'reports/report_create_template.html'
    http_method_names = ['post']

    def render_site(
            self, request, email_address, server_address, password):
        """ Render site without redirection to the other url
        """
        folder_list = get_mailbox_folder_list(
            server_address, email_address, password)

        return render(request, self.template_name, context={
            'folder_list': (folder.name for folder in folder_list),
            'mailbox':
                {'email_address': email_address,
                 'server_address': server_address,
                 'password': password},
                 'form': ReportGenerateForm()
        })

    # def post(self, request, *args, **kwargs):
    #     report_form = ReportGenerateForm(request.POST)

    #     if report_form.is_valid():


class MailboxValidateView(ValidateMailboxOwnerMixin, ValidateMailboxImapMixin, PassLoggedUserToFormMixin, generic.FormView):
    template_name = 'reports/mailbox_validate_template.html'
    form_class = MailboxValidateForm
    success_view = ReportCreateView
