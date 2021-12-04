from django.urls import path

from .views import (
    MailboxValidateView,
     ReportListView,
     ReportCreateView,
     ReportShowStatusView,
     ReportCheckStatusView)

urlpatterns = [
    path('list', ReportListView.as_view(), name='report_list_url'),
    path('create', ReportCreateView.as_view(), name='report_create_url'),
    path(
        'validate_mailbox',
        MailboxValidateView.as_view(),
     name='report_validate_mailbox_url'),
    path('<int:pk>/show_status',
         ReportShowStatusView.as_view(),
         name='report_show_status_url'),
    path('<int:pk>/check_status',
         ReportCheckStatusView.as_view(),
         name='report_check_status_url')
]
