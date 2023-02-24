import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from emailsystem.settings import BASE_DIR, MEDIA_URL, TEMPLATE_DIR

from .models import Email, EmailTemplate
from emailsystem.celery import app
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

@app.task(bind=True)
def send_dynamic_email(self, instance_id, template_id, context):
    try:
        instance = Email.objects.get(pk=instance_id)

        if template_id:
            try:
                template = EmailTemplate.objects.get(pk=template_id).template
                template = os.path.join(BASE_DIR, 'media/email_templates/email_eg.html')
                
            except EmailTemplate.DoesNotExist:
                instance.error_message = 'Template Does not exist.'
                instance.save()
                raise ObjectDoesNotExist(
                    'Template doesnot exist')
            
        else:
            template = os.path.join(TEMPLATE_DIR, 'default_email_template.html')

        html_content = render_to_string(template, context)
    
        bcc_email = context.get('bcc').split(
            ',') if context.get('bcc') != None else None
        cc_email = context.get('cc').split(',') if context.get('cc') != None else None
        to_email = context.get('recipient_emails').split(',') if context.get(
            'recipient_emails') != None else None

        message = EmailMultiAlternatives(
            subject=context.get('subject'), body=html_content, to=to_email, bcc=bcc_email , cc=cc_email)
        message.attach_alternative(html_content, "text/html")

        message.send()
    except Exception as e:
        instance.error_message = e
        instance.save()
    
    else:
        instance.delivered_at = datetime.now()
        instance.status = 'delivered'
        instance.save()
        
