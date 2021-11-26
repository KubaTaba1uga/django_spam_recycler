from django.views.generic.edit import FormMixin
from shared_code.queries import get_user_owner_mailboxes, get_user_guest_mailboxes
from shared_code.imap_sync import validate_credentials


class ShowMailboxGuestMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guest_mailboxes'] = get_user_guest_mailboxes(
            self.request.user)
        return context


class ShowMailboxOwnerMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner_mailboxes'] = get_user_owner_mailboxes(
            self.request.user)
        return context


class ValidateMailboxImapMixin(FormMixin):

    def form_valid(self, form):
        """ Validate mailbox by IMAP
        """
        if not validate_credentials(
            server_address=form.data.get('server_address'),
            email_address=form.data.get('email_address'),
                password=form.data.get('password')):

            form.add_error(None, 'Mailbox validation failed')

            return super().form_invalid(form)

        return super().form_valid(form)


class AddMailboxOwnerMixin(FormMixin):

        def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['initial']['owner'] = self.request.user
            return kwargs
