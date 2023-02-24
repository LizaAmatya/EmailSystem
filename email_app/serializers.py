from email_app.models import Email
from rest_framework import serializers

class EmailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Email
        fields = ['recipient_emails', 'subject', 'body', 'cc', 'bcc', 'email_template', 'signature']
        