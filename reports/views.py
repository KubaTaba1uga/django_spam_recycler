from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from mailboxes.mixins import PassLoggedUserToFormMixin
from shared_code.imap_sync import get_mailbox_folder_list, validate_credentials, validate_folder_list
from shared_code.queries import (
    count_messages_evaluations_in_report,
     count_messages_in_report,
     create_report,
     get_mailbox_by_owner,
    get_message_evaluation_by_id,
    get_report_by_id,
    get_report_by_id_and_owner,
     get_report_by_mailbox_and_name, get_message_by_id,
    get_report_details_template_data)
from .mixins import ShowOwnerReportsListMixin, ShowGuestReportsListMixin, ValidateMailboxImapMixin, ValidateMailboxOwnerMixin, ValidateReportOwnerMixin, ValidateReportOwnerOrGuestMixin
from .forms import MailboxValidateForm, ReportGenerateForm
from .tasks import generate_report_task
from .models import ReportModel


class ReportListView(LoginRequiredMixin, ShowOwnerReportsListMixin, ShowGuestReportsListMixin, generic.TemplateView):
    template_name = 'reports/report_list_template.html'


class ReportCreateView(LoginRequiredMixin, generic.View):
    template_name = 'reports/report_create_template.html'
    http_method_names = ['post']

    def render_site(
            self, request, email_address, server_address, password, form=ReportGenerateForm()):
        """ Render site without redirection to the other url
        """
        folder_list = get_mailbox_folder_list(
            {'email_address': email_address, 'server_address': server_address, 'password': password})

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
            """ If mailbox is valid it return logeed in imap Mailbox instance
                    Mailbox instance is reused in validate_folder_list function
                    to shorten HTTP response time of creation connections to IMAP server
            """
            imap_mailbox = validate_credentials(**mailbox_credentials)

            if imap_mailbox:

                if report_form.is_valid(request.user):

                    selected_folder_list = request.POST.getlist('folder')

                    if validate_folder_list(selected_folder_list, imap_mailbox,
                                            report_form):

                        """ Log out imap connection to avoid concurrency errors
                                imap_mailbox won't be needed anymore after this point
                        """
                        imap_mailbox.logout()

                        db_mailbox = get_mailbox_by_owner(
                            mailbox_credentials['email_address'],
                            request.user)

                        if db_mailbox:

                            if not get_report_by_mailbox_and_name(request.POST['name'], db_mailbox):
                                """ Generate report
                                """

                                report = create_report(
                                    request.POST[
                                        'name'], db_mailbox.id, request.POST['start_at'],
                                                      request.POST['end_at'])

                                generate_report_task.delay(
                                    request.user.id,
                                    selected_folder_list,
                                    request.POST['start_at'],
                                    request.POST['end_at'],
                                    mailbox_credentials,
                                    report.id
                                )

                                return redirect(reverse_lazy('reports:report_show_status_url', args=[report.id]))

                            else:
                                report_form.add_error(
                                    None,
                                    'Report with this name and mailbox already exists')

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


class MailboxValidateView(LoginRequiredMixin, ValidateMailboxOwnerMixin, ValidateMailboxImapMixin, PassLoggedUserToFormMixin, generic.FormView):
    template_name = 'reports/mailbox_validate_template.html'
    form_class = MailboxValidateForm
    success_view = ReportCreateView


class ReportShowStatusView(LoginRequiredMixin, ValidateReportOwnerOrGuestMixin, generic.TemplateView):
    template_name = 'reports/report_show_status_template.html'

    def get_context_data(self, **kwargs):
        context = super(ReportShowStatusView, self).get_context_data(**kwargs)
        context['report_id'] = kwargs.get('pk')
        return context


class ReportCheckStatusView(LoginRequiredMixin, ValidateReportOwnerOrGuestMixin, generic.View):

    def get(self, request, pk, *args, **kwargs):
        report = get_report_by_id_and_owner(pk, request.user.id)

        response_body = dict()

        if report:
            downloaded_messagess_counter = count_messages_in_report(report)

            evaluated_messagess_counter = count_messages_evaluations_in_report(
                report)

            response_body.update({
                'all_messagess_counter':
                report.messages_counter,
                'downloaded_messagess_counter':
                downloaded_messagess_counter,
                'evaluated_messagess_counter':
                evaluated_messagess_counter
            })

        else:
            raise Http404

        return JsonResponse(response_body)


class ReportIsReadyView(LoginRequiredMixin, ValidateReportOwnerOrGuestMixin, generic.View):

    def get(self, request, pk, *args, **kwargs):

        report = get_report_by_id(pk)

        if count_messages_in_report(report) == count_messages_evaluations_in_report(report) and report.messages_counter > 0:
            return redirect(reverse_lazy('reports:report_details_url', args=[pk]))
        else:
            return redirect(reverse_lazy('reports:report_show_status_url', args=[pk]))


class ReportDetailsView(LoginRequiredMixin, ValidateReportOwnerOrGuestMixin, generic.DetailView):
    template_name = 'reports/report_details_template.html'
    model = ReportModel
    context_object_name = 'report'

    def get_context_data(self, **kwargs):
        """ Get report messagess in one query
                to avoid long template rendering time
        """
        context = super().get_context_data(**kwargs)

        context['message_evaluation_list'] = get_report_details_template_data(
            self.object.id)

        return context


class ReportDeleteView(LoginRequiredMixin, ValidateReportOwnerMixin, generic.DeleteView):
    template_name = 'reports/report_delete_template.html'
    model = ReportModel
    context_object_name = 'report'
    success_url = reverse_lazy('reports:report_list_url')


class MessageShowView(LoginRequiredMixin, ValidateReportOwnerOrGuestMixin, generic.View):

        def get(self, request, pk, message_pk, *args, **kwargs):
            message = get_message_by_id(message_pk)

            if message:
                return HttpResponse(message.body)
            else:
                raise Http404


class MessageSpamEvaluationShowView(LoginRequiredMixin, ValidateReportOwnerOrGuestMixin, generic.View):

    def get(self, request, pk, evaluation_pk, *args, **kwargs):
        spam_evaluation = get_message_evaluation_by_id(evaluation_pk)

        if spam_evaluation:
            return HttpResponse(spam_evaluation.spam_description)
        else:
            raise Http404
