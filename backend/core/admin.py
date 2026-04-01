from django.contrib import admin
from .models import Campaign, Subscriber, EmailTemplate

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ["name", "campaign_type", "status", "sent_count", "open_rate", "created_at"]
    list_filter = ["campaign_type", "status"]
    search_fields = ["name"]

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "status", "list_name", "subscribed_date", "created_at"]
    list_filter = ["status"]
    search_fields = ["email", "name", "list_name"]

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "category", "active", "usage_count", "created_at"]
    list_filter = ["category"]
    search_fields = ["name", "subject"]
