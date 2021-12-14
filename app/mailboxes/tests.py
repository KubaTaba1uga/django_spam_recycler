from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django import asserts as pytest_asserts
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


class TestMailboxModel:

    @pytest.mark.django_db
    def test_mailbox_creation(self, create_mailbox):
        assert create_mailbox.email_address == MAILBOX['email_address']
        assert create_mailbox.server_address == MAILBOX['server_address']

    @pytest.mark.django_db
    def test_mailbox_representation(self, create_mailbox):
        assert str(create_mailbox) == MAILBOX['email_address']


class TestMailboxListView:
    SUCCESS_STATUS_CODE = 200
    FAIL_STATUS_CODE = 302
    URL = 'mailboxes:mailbox_list_url'
    TEMPLATE = 'mailboxes/mailbox_list_template.html'

    @pytest.mark.django_db
    def test_mailbox_list_success(self, client, create_user):
        client.force_login(create_user)
        response = client.get(reverse(self.URL))
        assert response.status_code == self.SUCCESS_STATUS_CODE

    @pytest.mark.django_db
    def test_mailbox_list_fail(self, client):
        response = client.get(reverse(self.URL))
        assert response.status_code == self.FAIL_STATUS_CODE

    @pytest.mark.django_db
    def test_mailbox_list_template(self, client, create_user):
        client.force_login(create_user)
        response = client.get(reverse(self.URL))
        pytest_asserts.assertTemplateUsed(response, self.TEMPLATE)
