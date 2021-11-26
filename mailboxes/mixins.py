from shared_code.queries import get_user_owner_mailboxes, get_user_guest_mailboxes


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
