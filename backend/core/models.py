from django.db import models

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    campaign_type = models.CharField(max_length=50, choices=[("newsletter", "Newsletter"), ("promotional", "Promotional"), ("drip", "Drip"), ("transactional", "Transactional")], default="newsletter")
    status = models.CharField(max_length=50, choices=[("draft", "Draft"), ("scheduled", "Scheduled"), ("sending", "Sending"), ("sent", "Sent"), ("paused", "Paused")], default="draft")
    sent_count = models.IntegerField(default=0)
    open_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    click_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    scheduled_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Subscriber(models.Model):
    email = models.EmailField(blank=True, default="")
    name = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("unsubscribed", "Unsubscribed"), ("bounced", "Bounced")], default="active")
    list_name = models.CharField(max_length=255, blank=True, default="")
    subscribed_date = models.DateField(null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email

class EmailTemplate(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True, default="")
    category = models.CharField(max_length=50, choices=[("welcome", "Welcome"), ("promo", "Promo"), ("newsletter", "Newsletter"), ("alert", "Alert"), ("transactional", "Transactional")], default="welcome")
    content = models.TextField(blank=True, default="")
    active = models.BooleanField(default=False)
    usage_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
