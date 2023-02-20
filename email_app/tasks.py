from .models import EmailTemplate
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from celery import shared_task


@shared_task
def send_dynamic_email(subject, to_email, template_name, context):
    template = EmailTemplate.objects.get(name=template_name)

    html_content = render_to_string(template.html_content, context)

    message = EmailMultiAlternatives(
        subject=subject, body=html_content, to=[to_email])
    message.attach_alternative(html_content, "text/html")

    message.send()
