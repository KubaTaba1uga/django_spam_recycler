from django.urls import path

from .views import (
    MailboxValidateView,
    ReportListView,
    ReportCreateView,
    ReportShowStatusView,
    ReportCheckStatusView,
    ReportIsReadyView,
    ReportDetailsView,
    ReportDeleteView,
    MessageShowView,
    MessageSpamEvaluationShowView, DeleteWorkerTestView)

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
         name='report_check_status_url'),
    path(
        '<int:pk>/ready',
        ReportIsReadyView.as_view(),
        name='report_is_ready_url'),
    path('<int:pk>/details',
         ReportDetailsView.as_view(),
         name='report_details_url'),
    path('<int:pk>/delete',
         ReportDeleteView.as_view(),
         name='report_delete_url'),
    path('<int:pk>/details/<int:message_pk>/message',
         MessageShowView.as_view(),
         name='report_show_message_url'),
    path('<int:pk>/details/<int:evaluation_pk>/evaluation',
         MessageSpamEvaluationShowView.as_view(),
         name='report_show_message_evaluation_url'),
    path('delete/workers',
         DeleteWorkerTestView.as_view(),
         name='delete_worker_url'),


]
