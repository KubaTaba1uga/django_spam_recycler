from shared_code.name_utils import create_user_spam_queue_name
from subprocess import Popen, PIPE

SCRIPT_PATH = './scripts/set_up_user_queues.py'

COMMAND_EXEC = 'poetry run python'


def execute_command(command):
    return Popen(command.split(), stdout=PIPE)


def create_user_spam_queue(user_id):
    """
    Create a queue for each user
    """
    queue_name = create_user_spam_queue_name(user_id)
    execute_command(f'{COMMAND_EXEC} {SCRIPT_PATH} {user_id}')
    return queue_name
