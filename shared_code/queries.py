from mailboxes.models import MailboxModel, MailboxGuestModel


def get_user_guest_mailboxes(user):
    """
    Returns guest mailboxes of a user.
    """
    return (guest_mailbox.mailbox for guest_mailbox in MailboxGuestModel.objects.filter(guest=user).all())


def get_user_owner_mailboxes(user):
    """
    Returns owned mailboxes of a user.
    """
    return (owned_mailbox for owned_mailbox in MailboxModel.objects.filter(owner=user).all())
