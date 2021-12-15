from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django import asserts as pytest_asserts
import pytest
import os
from .models import MailboxModel, MailboxGuestModel
from shared_code.queries import get_mailbox_guests

USER = {
    'username': 'test',
    'email': 'test@test.pl',
    'password': '****************'
}

MAILBOX = {
    'email_address':
        os.environ.get('TEST_EMAIL_ADDRESS', 'jakub@lemonpro.eu'),
    'server_address':
        os.environ.get('TEST_SERVER_ADDRESS', 'Outlook.office365.com'),
    'password': os.environ.get('TEST_EMAIL_PASSWORD', '************'),
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


@pytest.fixture
@pytest.mark.django_db
def create_mailbox_guest(create_mailbox, create_user):
    return MailboxGuestModel.objects.create(guest=create_user, mailbox=create_mailbox)


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

    @pytest.mark.django_db
    def test_mailbox_list_content(self, client, create_user, create_mailbox):
        client.force_login(create_user)
        response = client.get(reverse(self.URL))
        assert create_mailbox.email_address in str(response.content)


class TestMailboxCreateView:
    SUCCESS_STATUS_CODE = 302
    FAIL_STATUS_CODE = 200
    URL = 'mailboxes:mailbox_create_url'
    TEMPLATE = 'mailboxes/mailbox_create_template.html'

    @pytest.mark.django_db
    def test_mailbox_create_success(self, client, create_user):
        client.force_login(create_user)
        MAILBOX['owner'] = create_user.pk
        response = client.post(reverse(self.URL), data=MAILBOX)
        assert response.status_code == self.SUCCESS_STATUS_CODE
        assert MailboxModel.objects.count() == 1

    @pytest.mark.django_db
    def test_mailbox_create_fail(self, client, create_user):
        client.force_login(create_user)
        response = client.post(reverse(self.URL), data={})
        assert response.status_code == self.FAIL_STATUS_CODE

    @pytest.mark.django_db
    def test_mailbox_create_template(self, client, create_user):
        client.force_login(create_user)
        response = client.get(reverse(self.URL))
        pytest_asserts.assertTemplateUsed(response, self.TEMPLATE)


class TestMailboxDetailsView:
    SUCCESS_STATUS_CODE = 200
    FAIL_STATUS_CODE = 403
    URL = 'mailboxes:mailbox_details_url'
    TEMPLATE = 'mailboxes/mailbox_details_template.html'

    @pytest.mark.django_db
    def test_mailbox_details_success(
            self, client, create_user, create_mailbox):

        client.force_login(create_user)

        response = client.get(
            reverse(self.URL, kwargs={'pk': create_mailbox.pk}))

        assert response.status_code == self.SUCCESS_STATUS_CODE

    @pytest.mark.django_db
    def test_mailbox_details_fail(
            self, client, create_user, create_mailbox):

        client.force_login(create_user)

        response = client.get(
            reverse(self.URL, kwargs={'pk': create_mailbox.pk + 100}))

        assert response.status_code == self.FAIL_STATUS_CODE

    @pytest.mark.django_db
    def test_mailbox_details_template(
            self, client, create_user, create_mailbox):

        client.force_login(create_user)

        response = client.get(
            reverse(self.URL, kwargs={'pk': create_mailbox.pk}))

        pytest_asserts.assertTemplateUsed(response, self.TEMPLATE)

    @pytest.mark.django_db
    def test_mailbox_details_content(
            self, client, create_user, create_mailbox):

        client.force_login(create_user)

        response = client.get(
            reverse(self.URL, kwargs={'pk': create_mailbox.pk}))

        assert create_mailbox.email_address in str(response.content)
        assert create_mailbox.server_address in str(response.content)
        assert create_mailbox.owner.username in str(response.content)


class TestMailboxInviteGuestView:
    SUCCESS_STATUS_CODE = 302
    FAIL_STATUS_CODE = 200
    URL = 'mailboxes:mailbox_invite_url'
    TEMPLATE = 'mailboxes/mailbox_add_guest_template.html'

    @pytest.mark.django_db
    def test_mailbox_invite_guest_success(
            self, client, create_user, create_mailbox):

        client.force_login(create_user)

        response = client.post(reverse(self.URL),
                               data={'mailbox': create_mailbox.pk,
                                     'guest': create_user.pk})

        assert response.status_code == self.SUCCESS_STATUS_CODE
        assert create_user in get_mailbox_guests(create_mailbox.pk)

    @pytest.mark.django_db
    def test_mailbox_invite_guest_failure(
            self, client, create_user, create_mailbox):

        client.force_login(create_user)

        response = client.post(reverse(self.URL),
                               data={'mailbox': create_mailbox.pk - 10,
                                     'guest': create_user.pk})

        assert response.status_code == self.FAIL_STATUS_CODE
        assert create_user not in get_mailbox_guests(create_mailbox.pk)

    @pytest.mark.django_db
    def test_mailbox_invite_guest_template(
            self, client, create_user, create_mailbox):

        client.force_login(create_user)

        response = client.get(reverse(self.URL))

        pytest_asserts.assertTemplateUsed(response, self.TEMPLATE)


class TestMailboxDeleteView:
    URL = 'mailboxes:mailbox_delete_url'
    TEMPLATE = 'mailboxes/mailbox_delete_template.html'

    @pytest.mark.django_db
    def test_mailbox_delete_success(
            self, client, create_user, create_mailbox):

        client.force_login(create_user)

        client.post(
            reverse(self.URL, kwargs={'pk': create_mailbox.pk}),
                               data={'mailbox': create_mailbox.pk})

        assert MailboxModel.objects.count() == 0

    @pytest.mark.django_db
    def test_mailbox_delete_failure(
            self, client, create_user, create_mailbox):

        client.force_login(create_user)

        client.post(
            reverse(self.URL, kwargs={'pk': create_mailbox.pk + 100}),
                               data={'mailbox': create_mailbox.pk + 100})

        assert MailboxModel.objects.count() == 1

    @pytest.mark.django_db
    def test_mailbox_delete_template(
            self, client, create_user, create_mailbox):

        client.force_login(create_user)

        response = client.get(
            reverse(self.URL, kwargs={'pk': create_mailbox.pk}))

        pytest_asserts.assertTemplateUsed(response, self.TEMPLATE)

    @pytest.mark.django_db
    def test_mailbox_delete_content(
            self, client, create_user, create_mailbox):

        client.force_login(create_user)

        response = client.get(
            reverse(self.URL, kwargs={'pk': create_mailbox.pk}))

        assert create_mailbox.email_address in str(response.content)
        assert "Delete Mailbox" in str(response.content)


class TestMailboxGuestDelete:
    URL = 'mailboxes:mailbox_guest_delete_url'
    TEMPLATE = 'mailboxes/mailbox_delete_guest_template.html'

    @pytest.mark.django_db
    def test_mailbox_guest_delete_success(
            self, client, create_user, create_mailbox, create_mailbox_guest):

        client.force_login(create_user)

        client.post(
            reverse(self.URL, kwargs={'pk': create_mailbox_guest.pk}),
                               data={'mailbox': create_mailbox_guest.pk})

        assert create_mailbox.guests.count() == 0

    @pytest.mark.django_db
    def test_mailbox_guest_delete_failure(
            self, client, create_user, create_mailbox, create_mailbox_guest):

        client.force_login(create_user)

        client.post(
            reverse(self.URL, kwargs={'pk': create_mailbox_guest.pk + 100}),
                               data={'mailbox': create_mailbox_guest.pk + 100})

        assert create_mailbox.guests.count() == 1

    @pytest.mark.django_db
    def test_mailbox_guest_delete_template(
            self, client, create_user, create_mailbox_guest):

        client.force_login(create_user)

        response = client.get(
            reverse(self.URL, kwargs={'pk': create_mailbox_guest.pk}))

        pytest_asserts.assertTemplateUsed(response, self.TEMPLATE)

    @pytest.mark.django_db
    def test_mailbox_guest_delete_content(
            self, client, create_user, create_mailbox_guest):

        client.force_login(create_user)

        response = client.get(
            reverse(self.URL, kwargs={'pk': create_mailbox_guest.pk}))

        assert create_mailbox_guest.guest.username in str(response.content)
        assert "Delete Guest" in str(response.content)
