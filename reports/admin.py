from django.contrib import admin
from .models import ReportModel, MessageModel

admin.site.register([ReportModel, MessageModel])
