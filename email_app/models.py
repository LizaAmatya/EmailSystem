from django.db import models

class EmailTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)
    template = models.FileField(upload_to='email_templates/')
    

EMAIL_STATUS = [
    ("draft", "Draft"),
    ("sent", "Sent"),
    ("delivered", "Delivered"),
    ("failed","Failed")
]

class Email(models.Model):
    created_date = models.DateTimeField(blank=True, auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, auto_now=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    sender_email = models.CharField(max_length=255, blank=False, null=True)
    recipient_emails = models.TextField(blank=False, null=True)
    subject = models.TextField(blank=False, null=True)
    body = models.TextField(blank=True, null=True)
    cc = models.TextField(blank=True, null=True)
    bcc = models.TextField(blank=True, null=True)
    email_template = models.ForeignKey(
        'EmailTemplate', on_delete=models.PROTECT, related_name='email_template', null=True, blank=True)
    status = models.CharField(max_length=20, choices=EMAIL_STATUS, default='draft')
    signature = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
