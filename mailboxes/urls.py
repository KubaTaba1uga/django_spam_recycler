from django.urls import path

from .views import MailboxListView

urlpatterns = [
    path('list', MailboxListView.as_view(), name='mailbox_list_url'),
]
