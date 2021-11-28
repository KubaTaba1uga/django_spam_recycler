from django.views import generic
from .models import ReportModel


class ReportListView(generic.ListView):
    template_name = 'reports/report_list_template.html'
    model = ReportModel
    context_object_name = 'report_list'
