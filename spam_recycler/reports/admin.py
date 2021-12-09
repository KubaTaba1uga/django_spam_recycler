from django.contrib import admin
from .models import ReportModel, MessageModel, MessageEvaluationModel

admin.site.register([ReportModel, MessageModel, MessageEvaluationModel])
