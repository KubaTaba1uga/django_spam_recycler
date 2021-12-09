from imap_tools.errors import MailboxFolderSelectError
from imap_tools import MailBox, AND
import logging
import datetime


def validate_credentials(email_address, server_address, password):
    """Validate IMAP credentials.
        If IMAP validation succeed
         return True

    Args:
        URL (str): [address to which app will connect to, using IMAP]
        email_address (str): [username which app should validate]
        password (str): [password which app should validate]

    Returns:
        [MailBox/bool]: [MailBox if credentials are valid,
                  False if credentials are not valid]
    """

    try:
        return MailBox(server_address).login(email_address, password)
    except Exception as e:
        logging.warning(f"Validate creadentials failed - {e}\n email address: {email_address}\n server address {server_address}")
    """ Because exceptions types thrown by `imap_tools` are not predictible,
            `Exception` is used

        Code before:
            except ConnectionRefusedError:
                pass
             except IMAP4.error:
                pass
             except MailboxLoginError:
                pass
    """
    return False


def create_search_from_str(start_at, end_at):
    """ Str formats:
        start_at: "YYYY-MM-DD"
          end_at: "YYYY-MM-DD"
    """
    start_date_list = start_at.split('-')
    end_date_list = end_at.split('-')

    start_at_date = datetime.date(
        int(start_date_list[0]),
        int(start_date_list[1]),
     int(start_date_list[2]))

    end_at_date = datetime.date(
        int(end_date_list[0]),
        int(end_date_list[1]),
     int(end_date_list[2]))

    return AND(
        AND(date_gte=start_at_date),
        AND(date_lt=end_at_date))


def create_mailbox(email_address, server_address, password):
    return MailBox(server_address).login(
        email_address, password)


def validate_folder(mailbox, folder):
    """Chack folder exsistance, inside mailbox
        If folder validation succeed
         return True else False

    Args:
        mailbox (imap_tools.MailBox): [mailbox which app use to check folder exsistance]
        folder_name (str): [folder which app validate]


    Returns:
        [bool]: [True if folder exsist in mailbox,
                  False if not]
    """
    try:
        mailbox.folder.set(folder)
    except MailboxFolderSelectError:
        return False
    return True


def validate_folder_list(folder_list, mailbox, form):
    """Validate folders list for report usage
        in case of error, add them to `form` object
    """
    if len(folder_list) == 0:
        form.add_error(None, 'No folder selected')
    else:
        for folder in folder_list:
            if not validate_folder(mailbox, folder):
                form.add_error(None,
                               f'Folder: {folder}\n is unavailable for scan')
    if len(form.errors) == 0:
        return True
    else:
        return False


def create_mailbox_decorator(func):
    """ If function use Mailbox object,
            use decorator to avoid creating MailBox object
            inside function

        Example:
            Without decorator

                def get_mailbox_folder_list(email_address, server_address, password):
                    mailbox = create_mailbox(email_address, server_address, password)
                    folder_list = mailbox.folder.list()
                    mailbox.logut()
                    return folder_list

            With decorator

                @create_mailbox_decorator
                def get_mailbox_folder_list(mailbox):
                    return mailbox.folder.list()


    """
    def decorator(mailbox_credentials, *args, **kwargs):

        mailbox = create_mailbox(**mailbox_credentials)

        result = func(mailbox, *args, **kwargs)

        mailbox.logout()

        return result

    return decorator


@create_mailbox_decorator
def get_mailbox_folder_list(mailbox):
    folder_list = mailbox.folder.list()
    return folder_list


@create_mailbox_decorator
def gather_emails_GUIDs(mailbox, search, folder):
    """ Download GUID of messages passing search requirements
    """
    mailbox.folder.set(folder)
    return (email for email in mailbox.uids(search))


@create_mailbox_decorator
def download_message_by_guid(mailbox, guid):
    for email in mailbox.fetch(AND(uid=[guid])):
        return email


def parse_message(message):
    return {
        'subject': message.subject,
        'sender': message.from_values.email,
        'to_recipients': " ,".join(to.email for to in message.to_values),
        'received_at': message.date,
        'body': message.html,
        'orginal_message': message.obj
    }
