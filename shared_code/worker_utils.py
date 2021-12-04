from shared_code.name_utils import create_user_spam_queue_name, create_user_email_queue_name
from subprocess import Popen, PIPE

SCRIPT_PATH = './scripts/set_up_user_queues.py'

COMMAND_EXEC = 'poetry run python'


def execute_command(command):
    process = Popen(command.split(), stdout=PIPE)
    if process.wait() != 0:
        raise Exception(f'Error executing command: {command}')


def create_user_spam_queue(user_id):
    """
    Create a queue for each user
    """
    queue_name = create_user_spam_queue_name(user_id)
    execute_command(f'{COMMAND_EXEC} {SCRIPT_PATH} {user_id} spam')
    return queue_name


def create_user_email_queue(user_id):
    """
    Create a queue for each user
    """
    queue_name = create_user_spam_queue_name(user_id)
    execute_command(f'{COMMAND_EXEC} {SCRIPT_PATH} {user_id} email')
    return queue_name
