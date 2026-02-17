# cache/tasks.py
from celery import shared_task
from tenants.models import Tenant
from utils.sms_api import SMSAPIClient
from .models import CachedNews, CachedEvent, CachedNotice

@shared_task
def sync_news_for_tenant(tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    client = SMSAPIClient(tenant)
    page = 1
    while True:
        data = client.get_news(page=page, limit=100)
        for item in data['results']:
            CachedNews.objects.update_or_create(
                tenant=tenant,
                sms_id=item['id'],
                defaults={
                    'title': item['title'],
                    'content': item['content'],
                    # ... ম্যাপিং
                }
            )
        if not data.get('next'):
            break
        page += 1

@shared_task
def sync_all_tenants_news():
    for tenant in Tenant.objects.all():
        sync_news_for_tenant.delay(tenant.id)