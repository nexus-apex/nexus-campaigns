from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Campaign, Subscriber, EmailTemplate
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusCampaigns with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexuscampaigns.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Campaign.objects.count() == 0:
            for i in range(10):
                Campaign.objects.create(
                    name=f"Sample Campaign {i+1}",
                    campaign_type=random.choice(["newsletter", "promotional", "drip", "transactional"]),
                    status=random.choice(["draft", "scheduled", "sending", "sent", "paused"]),
                    sent_count=random.randint(1, 100),
                    open_rate=round(random.uniform(1000, 50000), 2),
                    click_rate=round(random.uniform(1000, 50000), 2),
                    scheduled_date=date.today() - timedelta(days=random.randint(0, 90)),
                )
            self.stdout.write(self.style.SUCCESS('10 Campaign records created'))

        if Subscriber.objects.count() == 0:
            for i in range(10):
                Subscriber.objects.create(
                    email=f"demo{i+1}@example.com",
                    name=f"Sample Subscriber {i+1}",
                    status=random.choice(["active", "unsubscribed", "bounced"]),
                    list_name=f"Sample Subscriber {i+1}",
                    subscribed_date=date.today() - timedelta(days=random.randint(0, 90)),
                    tags=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Subscriber records created'))

        if EmailTemplate.objects.count() == 0:
            for i in range(10):
                EmailTemplate.objects.create(
                    name=f"Sample EmailTemplate {i+1}",
                    subject=f"Sample EmailTemplate {i+1}",
                    category=random.choice(["welcome", "promo", "newsletter", "alert", "transactional"]),
                    content=f"Sample content for record {i+1}",
                    active=random.choice([True, False]),
                    usage_count=random.randint(1, 100),
                )
            self.stdout.write(self.style.SUCCESS('10 EmailTemplate records created'))
