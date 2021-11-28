from django.views.generic.edit import FormMixin
from django.core.exceptions import PermissionDenied
from shared_code.queries import get_user_owner_reports, get_user_guest_reports, get_mailbox_query, get_mailbox_owner
from shared_code.imap_sync import validate_credentials


class ShowOwnerReportsListMixin:

    """ Show reports of mailbox for which user is owner
    """

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['owner_reports'] = get_user_owner_reports(
            self.request.user)
        return context


class ShowGuestReportsListMixin:

    """ Show reports of mailbox for which user is guest
    """

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['guest_reports'] = get_user_guest_reports(
            self.request.user)
        return context


class ValidateMailboxImapMixin(FormMixin):

    """ Validate IMAP connection
    """

    def get_form_kwargs(self):
        """ Add mailbox parameters to form instance
        """
        form_data = super().get_form_kwargs()
        if form_data.get('data') and form_data['data'].get('email_address'):

            mailbox_id = form_data['data'].get('email_address')

            mailbox = get_mailbox_query(mailbox_id)

            self.email_address = mailbox.email_address
            self.email_server_address = mailbox.server_address
            self.email_password = form_data['data'].get('password')

        return form_data

    def form_valid(self, form):
        mailbox_credentials = {
            'server_address': self.email_server_address,
            'email_address': self.email_address,
            'password': self.email_password}

        if validate_credentials(
                **mailbox_credentials):
            """
                If mailbox is valid, render report
                generation form with valid data
            """
            return self.success_view().render_site(self.request, **mailbox_credentials)

        form.add_error(None, 'Mailbox validation failed')

        return super().form_invalid(form)


class ValidateMailboxOwnerMixin(FormMixin):

    def form_valid(self, form):
        mailbox_id = form.data.get('email_address', 0)

        if not get_mailbox_owner(mailbox_id) == self.request.user:
            raise PermissionDenied('You are not owner of this mailbox')

        return super().form_valid(form)
