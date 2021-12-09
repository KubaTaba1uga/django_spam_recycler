from django.conf import settings
from django.contrib import admin
from django.urls import path, include

MAILBOXES_APP = ('mailboxes.urls', 'mailboxes')
REPORTS_APP = ('reports.urls', 'reports')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('pages.urls')),
    path('mailbox/', include(MAILBOXES_APP, namespace='mailbox')),
    path('report/', include(REPORTS_APP, namespace='report')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
