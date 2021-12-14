from django.contrib.auth import get_user_model
import pytest
import os

from .models import MailboxModel

USER = {
    'username': 'test',
    'email': 'test@test.pl',
    'password': '****************'
}

MAILBOX = {
    'email_address':
        os.environ.get('TEST_EMAIL_ADDRESS', 'jakub.buczynski@example.com'),
    'server_address':
        os.environ.get('TEST_SERVER_ADDRESS', 'imap.example.com'),
    'password': os.environ.get('TEST_EMAIL_PASSWORD', '****************'),
}


@pytest.fixture
@pytest.mark.django_db
def create_user():
    return get_user_model().objects.create(**USER)


@pytest.fixture
@pytest.mark.django_db
def create_mailbox(create_user):
    return MailboxModel.objects.create(
        owner=create_user,
            email_address=MAILBOX['email_address'],
            server_address=MAILBOX['server_address'])


@pytest.mark.django_db
def test_mailbox_creation(create_mailbox):
    assert create_mailbox.email_address == MAILBOX['email_address']
    assert create_mailbox.server_address == MAILBOX['server_address']


@pytest.mark.django_db
def test_mailbox_representation(create_mailbox):
    assert str(create_mailbox) == MAILBOX['email_address']
