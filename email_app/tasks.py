import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from emailsystem.settings import MEDIA_ROOT, TEMPLATE_DIR

from .models import Email, EmailTemplate
from emailsystem.celery import app
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


def get_template_path(template_id):
    if template_id:
        try:
            template = EmailTemplate.objects.get(pk=template_id).template
            return os.path.join(MEDIA_ROOT, template.name)
        except EmailTemplate.DoesNotExist:
            raise ObjectDoesNotExist('Template does not exist')
    else:
        return os.path.join(TEMPLATE_DIR, 'default_email_template.html')


@app.task(bind=True)
def send_dynamic_email(self, instance_id, template_id, context):
    
    instance = Email.objects.get(pk=instance_id)

    template_path = get_template_path(template_id)

    html_content = render_to_string(template_path, context)

    bcc_email = context.get('bcc').split(
        ',') if context.get('bcc') != None else None
    cc_email = context.get('cc').split(
        ',') if context.get('cc') != None else None
    to_email = context.get('recipient_emails').split(',') if context.get(
        'recipient_emails') != None else None

    message = EmailMultiAlternatives(
        subject=context.get('subject'), 
        body=html_content, 
        to=to_email, bcc=bcc_email, cc=cc_email)
    message.attach_alternative(html_content, "text/html")

    try:
        message.send()
    except Exception as e:
        instance.error_message = str(e)
    else:
        instance.delivered_at = datetime.now()
        instance.status = 'delivered'

    instance.save()
    