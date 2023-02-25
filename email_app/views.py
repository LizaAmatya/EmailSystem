from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from emailsystem.settings import EMAIL_HOST_USER, TEMPLATE_DIR
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from email_app.filters import EmailFilter
from email_app.models import Email
from email_app.serializers import EmailSerializer
from email_app.tasks import send_dynamic_email
from datetime import datetime

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

        context.pop('email_template')
        send_email = send_dynamic_email.delay(
            instance.pk, template, dict(context))
        headers = self.get_success_headers(serializer.data)
        return Response({'message': "Email sent."}, status=status.HTTP_201_CREATED, headers=headers)


class EmailList(ListAPIView):
    serializer_class = EmailSerializer
    queryset = Email.objects.all()
    pagination_class = PageNumberPagination
    # filter_backends = [DjangoFilterBackend]
    # filtset_class = EmailFilter
    # filterset_fields = ['recipient_emails']
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        query_params = self.request.query_params
        
        from_date = query_params.get('from_date')
        to_date = query_params.get('to_date')
        email_address = query_params.get('email_address')
        
        if to_date == None:
            to_date = datetime.today()
        
        if email_address:
            qs = qs.filter(recipient_emails__contains=email_address)
            
        if from_date:
            qs = qs.filter(created_date__date__gte=from_date, created_date__date__lte=to_date)
        
        return qs
    

class MarkReadUnread(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        try:
            instance = Email.objects.get(id=self.kwargs['pk'])
            instance.is_read = not instance.is_read
            instance.save()

            if instance.is_read:
                message = 'Email marked read'
            else:
                message = 'Email marked unread'
                
            code = status.HTTP_200_OK

        except ObjectDoesNotExist:
            message = f"Email object with id {self.kwargs['id']} does not exist."
            code = status.HTTP_404_NOT_FOUND

        return Response({"msg": message}, status=code)
