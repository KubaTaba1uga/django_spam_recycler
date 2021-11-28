from shared_code.queries import get_user_owner_reports, get_user_guest_reports


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
