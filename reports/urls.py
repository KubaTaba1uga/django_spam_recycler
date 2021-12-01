from django.urls import path

from .views import MailboxValidateView, ReportListView, ReportCreateView, TestRabbitMqView

urlpatterns = [
    path('list', ReportListView.as_view(), name='report_list_url'),
    path('create', ReportCreateView.as_view(), name='report_create_url'),
    path(
        'validate_mailbox',
        MailboxValidateView.as_view(),
     name='report_validate_mailbox_url'),
     path('test', TestRabbitMqView.as_view()),
]
