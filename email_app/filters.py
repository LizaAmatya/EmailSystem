from django_filters import rest_framework as filters
from email_app.models import Email

class EmailFilter(filters.FilterSet):
    start_date = filters.DateFilter(
        field_name="created_at", lookup_expr='gte',  input_formats=["%Y-%m-%d", "%d-%m-%Y"],)
    end_date = filters.DateFilter(
        field_name="created_at", lookup_expr='lte',  input_formats=["%Y-%m-%d", "%d-%m-%Y"],)
    email_address = filters.CharFilter(
        field_name="recipient_emails", lookup_expr="contains")
    
    class Meta:
        model = Email
        fields = ['recipient_emails']
