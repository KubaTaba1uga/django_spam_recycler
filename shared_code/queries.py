from mailboxes.models import MailboxModel, MailboxGuestModel


def get_user_guest_mailboxes(user):
    """
    Returns guest mailboxes of a user.
    """
    return (guest_mailbox.mailbox for guest_mailbox in MailboxGuestModel.objects.filter(guest=user).all())


def get_user_owner_mailboxes_query(user):
    return MailboxModel.objects.filter(owner=user).all()


def get_user_owner_mailboxes(user):
    """
    Return owned mailboxes of a user.
    """
    return (owned_mailbox for owned_mailbox in get_user_owner_mailboxes_query(user))


def get_user_owner_mailboxes_tuples(user):
    """
    Return owned mailboxes of a user as tuple
        example:
            (instance.email_address, instance)
    """
    return ((owned_mailbox.email_address, owned_mailbox) for owned_mailbox in get_user_owner_mailboxes_query(user))


def get_mailbox_query(mailbox_id):
    return MailboxModel.objects.filter(pk=mailbox_id).first()


def get_mailbox_owner(mailbox_id):
    """
    Return owner of a mailbox or None if mailbox does not exist
    """
    mailbox = get_mailbox_query(mailbox_id)
    if mailbox:
        return mailbox.owner


def get_mailbox_guests_query(mailbox_id):
    return MailboxGuestModel.objects.filter(mailbox_id=mailbox_id).all()


def get_mailbox_guests(mailbox_id):
    """ Return all guests of mailbox with provided id
    """
    return (guest_mailbox.guest for guest_mailbox in get_mailbox_guests_query(mailbox_id))


def get_guest_mailbox(mailbox_id):
    """
    Return all guest mailboxes of mailbox with provided id
    """
    return (guest_mailbox for guest_mailbox in get_mailbox_guests_query(mailbox_id))


def get_guest(guest_id):
    """
    Return all guest mailboxes of mailbox with provided id
    """

    return MailboxGuestModel.objects.filter(pk=guest_id).first()


def get_user_owner_reports(user):
    """
    Return all reports of user owned mailboxes
    """

    for mailbox in get_user_owner_mailboxes(user):
        for report in mailbox.report.all():
            yield report


def get_user_guest_reports(user):
    """
    Return all reports of user guest mailboxes
    """
    for mailbox in get_user_guest_mailboxes(user):
        for report in mailbox.report.all():
            yield report
