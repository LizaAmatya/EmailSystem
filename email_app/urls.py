from django.urls import path

from email_app.views import SendEmail

app_name = 'email'

urlpatterns = [
    path('send', SendEmail.as_view(), name='send_email')
]
