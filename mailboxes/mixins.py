from django.views.generic.edit import FormMixin
from shared_code.queries import (
    get_user_owner_mailboxes,
     get_user_guest_mailboxes,
     get_mailbox_owner,
     get_guest_mailbox,
     get_mailbox_guests,
     get_guest)
from shared_code.imap_sync import validate_credentials
from django.core.exceptions import PermissionDenied


class ShowGuestMailboxListMixin:

    """
    Show mailboxes which user is guest of
    """

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['guest_mailboxes'] = get_user_guest_mailboxes(
            self.request.user)
        return context


class ShowOwnerMailboxListMixin:

    """
    Show mailboxes which user is owner of
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner_mailboxes'] = get_user_owner_mailboxes(
            self.request.user)
        return context


class ValidateMailboxImapMixin(FormMixin):

    """
    Validate mailbox by IMAP
    """

    def form_valid(self, form):
        if not validate_credentials(
            server_address=form.data.get('server_address'),
            email_address=form.data.get('email_address'),
                password=form.data.get('password')):

            form.add_error(None, 'Mailbox validation failed')

            return super().form_invalid(form)

        return super().form_valid(form)


class AddMailboxOwnerMixin(FormMixin):

    def get_form_kwargs(self):
        """ Add logged in user as initial `owner` value
        """
        kwargs = super().get_form_kwargs()
        kwargs['initial']['owner'] = self.request.user
        return kwargs


class AddOwnedMailboxMixin(FormMixin):

    def get_form_kwargs(self):
        """ Add logged in user as initial `owner` value
        """
        kwargs = super().get_form_kwargs()
        kwargs['initial']['mailbox'] = get_user_owner_mailboxes(
            self.request.user)
        return kwargs


class PassLoggedUserToFormMixin(FormMixin):

    def get_form_kwargs(self):
        """ Pass logged in user to form
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailboxOwnerOnlyMixin:

    def dispatch(self, request, *args, **kwargs):
        """ Allow user if is owner of mailbox
        """

        if not get_mailbox_owner(self.kwargs.get('pk', 0)) == self.request.user:
            raise PermissionDenied('You are not owner of this mailbox')

        return super().dispatch(request, *args, **kwargs)


class MailboxOwnerAndGuestOnlyMixin:

    def dispatch(self, request, *args, **kwargs):
        """ Allow user if is owner or guest of mailbox
        """
        mailbox_id = self.kwargs.get('pk', 0)

        is_owner = get_mailbox_owner(mailbox_id) == self.request.user

        is_guest = self.request.user in get_mailbox_guests(mailbox_id)

        if is_owner or is_guest:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class GuestMailboxOwnerOnlyMixin:

    def dispatch(self, request, *args, **kwargs):
        """ Allow user if is owner of guest_mailbox
        """

        guest_mailbox = get_guest(self.kwargs.get('pk'))

        if guest_mailbox and guest_mailbox.mailbox.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class ShowMailboxGuestsMixin:

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['mailbox_guests'] = get_guest_mailbox(
                self.kwargs.get('pk', 0))
            return context
