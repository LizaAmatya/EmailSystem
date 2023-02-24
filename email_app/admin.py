from django.contrib import admin

from email_app.models import Email, EmailTemplate

# Register your models here.


class EmailAdmin(admin.ModelAdmin):
    list_display = ['sender_email', 'subject',
                    'delivered_at', 'status']

admin.site.register(EmailTemplate)
admin.site.register(Email,EmailAdmin)
