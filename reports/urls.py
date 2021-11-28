from django.urls import path

from .views import ReportListView

urlpatterns = [
    path('list', ReportListView.as_view(), name='report_list_url')
]
