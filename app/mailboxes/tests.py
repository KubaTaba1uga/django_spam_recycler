from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from .models import MailboxModel
import os

USER = {
    'username': 'test',
    'email': 'test@test.pl',
    'password': '****************'
}

MAILBOX = {
    'email_address': os.environ.get('TEST_EMAIL_ADDRESS'),
    'server_address': os.environ.get('TEST_SERVER_ADDRESS'),
    'password': os.environ.get('TEST_EMAIL_PASSWORD'),
}


class MailboxModelTest(TransactionTestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(**USER)

        self.mailbox = MailboxModel.objects.create(
            owner=self.user,
            **MAILBOX)

    def test_mailbox_creation(self):
        self.assertTrue(
            MailboxModel.objects.filter(owner=self.user, **MAILBOX).exists())

    def test_mailbox_content(self):
        self.assertTrue(
            MailboxModel.objects.filter(
                owner=self.user,
                **MAILBOX))

    def test_mailbox_representation(self):
        self.assertEqual(str(self.mailbox), MAILBOX['email_address'])
