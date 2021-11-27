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
    Returns owned mailboxes of a user.
    """
    return (owned_mailbox for owned_mailbox in get_user_owner_mailboxes_query(user))


def get_mailbox_owner_query(mailbox_id):
    return MailboxModel.objects.filter(pk=mailbox_id).first().owner


def get_mailbox_owner(mailbox_id):
    return get_mailbox_owner_query(mailbox_id)


def get_mailbox_guests_query(mailbox_id):
    return MailboxGuestModel.objects.filter(mailbox_id=mailbox_id).all()


def get_mailbox_guests(mailbox_id):
    return (guest_mailbox.guest for guest_mailbox in get_mailbox_guests_query(mailbox_id))
