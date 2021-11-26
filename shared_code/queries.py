from mailboxes.models import MailboxModel, MailboxGuestModel


def get_user_guest_mailboxes(user):
    """
    Returns a list of mailboxes for a user.
    """
    return (guest_mailbox.mailbox for guest_mailbox in MailboxGuestModel.objects.filter(guest=user).all())


def get_user_owner_mailboxes(user):
    return MailboxModel.objects.filter(owner=user).all()
