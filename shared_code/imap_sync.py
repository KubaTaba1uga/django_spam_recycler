from imap_tools import MailBox
import logging


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


def get_mailbox_folder_list(server_address, email_address, password):
    return MailBox(server_address).login(
        email_address, password).folder.list()
