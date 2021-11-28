from django.urls import path

from .views import ReportListView, ReportCreateView

urlpatterns = [
    path('list', ReportListView.as_view(), name='report_list_url'),
    path('create', ReportCreateView.as_view(), name='report_create_url')
]
