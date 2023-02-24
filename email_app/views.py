from email_app.models import Email
from email_app.serializers import EmailSerializer
from email_app.tasks import send_dynamic_email
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from emailsystem.settings import TEMPLATE_DIR, EMAIL_HOST_USER


class SendEmail(CreateAPIView):
    model = Email
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(sender_email=EMAIL_HOST_USER, status='sent')
        context = serializer.validated_data
       
        template = None
        if instance.email_template:
            template = instance.email_template.pk
            
        print('template vls!!!!', template)
        context.pop('email_template')
        send_email = send_dynamic_email.delay(instance.pk, template, dict(context))
        headers = self.get_success_headers(serializer.data)
        return Response({'message': "Email sent."}, status=status.HTTP_201_CREATED, headers=headers)
