from django.contrib import admin
from .models import MailboxModel, MailboxGuestModel

admin.site.register([MailboxModel, MailboxGuestModel])
