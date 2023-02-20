from .models import EmailTemplate
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render

# def load_email_template(template_name):
#     template_dir = os.path.join(TEMPLATES_DIR, template_name)
#     template_path = os.path.join(template_dir, template_name)
#     with open(template_path) as f:
#         template = f.read()
#     return template


def send_dynamic_email(subject, to_email, template_name, context):
    # Retrieve the email template from the database
    template = EmailTemplate.objects.get(name=template_name)

    # Render the HTML content of the template with the given context
    html_content = render_to_string(template.html_content, context)

    # Create the email message with both HTML and plain text content
    message = EmailMultiAlternatives(
        subject=subject, body=html_content, to=[to_email])
    message.attach_alternative(html_content, "text/html")

    # Send the email
    message.send()
