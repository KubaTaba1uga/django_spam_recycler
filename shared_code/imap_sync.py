from imap_tools import MailBox, AND
from imap_tools.mailbox import MailboxLoginError
from imaplib import IMAP4


def validate_credentials(server_address, email_address, password):
    """Validate IMAP credentials.
        If IMAP validation succeed
         return True

    Args:
        URL (str): [address to which app will connect to, using IMAP]
        email_address (str): [username which app should validate]
        password (str): [password which app should validate]

    Returns:
        [bool]: [True if credentials are valid,
                  False if credentials are not valid]
    """

    try:
        return MailBox(server_address).login(email_address, password)
    except ConnectionRefusedError as e:
        pass
    except IMAP4.error as e:
        pass
    except MailboxLoginError as e:
        pass

    return False
