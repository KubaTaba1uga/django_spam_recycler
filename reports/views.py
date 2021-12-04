from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from mailboxes.mixins import PassLoggedUserToFormMixin
from shared_code.imap_sync import get_mailbox_folder_list, validate_credentials, validate_folder_list
from shared_code.queries import get_mailbox_by_owner
from .mixins import ShowOwnerReportsListMixin, ShowGuestReportsListMixin, ValidateMailboxImapMixin, ValidateMailboxOwnerMixin
from .forms import MailboxValidateForm, ReportGenerateForm
from .tasks import generate_report_task


class ReportListView(ShowOwnerReportsListMixin, ShowGuestReportsListMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = 'reports/report_list_template.html'


class ReportCreateView(LoginRequiredMixin, generic.View):
    template_name = 'reports/report_create_template.html'
    http_method_names = ['post']

    def render_site(
            self, request, email_address, server_address, password, form=ReportGenerateForm()):
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
                 'form': form
        })

    def post(self, request, *args, **kwargs):
        report_form = ReportGenerateForm(request.POST)

        mailbox_credentials = {
            'email_address': request.POST.get('email_address'),
                'server_address': request.POST.get('server_address'),
                'password': request.POST.get('password')
        }

        if mailbox_credentials['email_address'] and mailbox_credentials['server_address'] and mailbox_credentials['password']:

            imap_mailbox = validate_credentials(**mailbox_credentials)

            if imap_mailbox:

                if report_form.is_valid(request.user):

                    selected_folder_list = request.POST.getlist('folder')

                    if validate_folder_list(selected_folder_list, imap_mailbox,
                                            report_form):

                        db_mailbox = get_mailbox_by_owner(
                            mailbox_credentials['email_address'],
                            request.user)

                        if db_mailbox:
                            """ TO-DO
                            Add report validation here
                            """

                            generate_report_task.delay(
                                request.user.id,
                                selected_folder_list,
                                **mailbox_credentials
                            )

                            # report = create_report(
                            #     report_form.cleaned_data['name'],
                            #     db_mailbox,
                            #     request.user,
                            #     report_form.cleaned_data['start_at'],
                            #     report_form.cleaned_data['end_at'])

                            if True:
                                """ Generate report
                                """

                            else:
                                report_form.add_error(
                                    None,
                                    'Report creation failed')

                        else:
                            report_form.add_error(
                                None,
                                'You are not the owner of the mailbox')

                    else:
                        report_form.add_error(None, 'Folder validation failed')

            else:
                report_form.add_error(None, 'Mailbox validation failed')

        else:
            report_form.add_error(None, 'Mailbox validation failed')

        return self.render_site(request, **mailbox_credentials, form=report_form)


class MailboxValidateView(ValidateMailboxOwnerMixin, ValidateMailboxImapMixin, PassLoggedUserToFormMixin, LoginRequiredMixin, generic.FormView):
    template_name = 'reports/mailbox_validate_template.html'
    form_class = MailboxValidateForm
    success_view = ReportCreateView
