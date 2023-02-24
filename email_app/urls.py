from django.urls import path

from email_app.views import EmailList, SendEmail, MarkReadUnread

app_name = 'email'

urlpatterns = [
    path('send', SendEmail.as_view(), name='send_email'),
    path('', EmailList.as_view(), name='email-list'),
    path('read/<int:pk>', MarkReadUnread.as_view(), name='mark-read')
]
