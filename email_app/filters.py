from django_filters import rest_framework as filters
from email_app.models import Email

class EmailFilter(filters.FilterSet):
    from_date = filters.DateFilter(
        field_name="created_date", lookup_expr='gte')
    to_date = filters.DateFilter(
        field_name="created_date", lookup_expr='lte')
    email_address = filters.CharFilter(
        field_name="recipient_emails", lookup_expr="contains")
    
    class Meta:
        model = Email
        fields = ['recipient_emails', 'from_date', 'to_date', 'email_address']
