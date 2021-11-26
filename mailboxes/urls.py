from django.urls import path

from .views import MailboxListView, MailboxCreateView, MailboxDetailsView

urlpatterns = [
    path('list', MailboxListView.as_view(), name='mailbox_list_url'),
    path('create', MailboxCreateView.as_view(), name='mailbox_create_url'),
    path(
        '<int:pk>/detail',
        MailboxDetailsView.as_view(),
     name='mailbox_details_url'),
]
