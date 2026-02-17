import httpx
from django.conf import settings
import asyncio

class SMSAPIClient:
    def __init__(self, tenant):
        self.base_url = tenant.api_base_url.rstrip('/')
        self.api_key = tenant.api_key
        self.api_secret = tenant.api_secret
        self.tenant_id = tenant.sms_tenant_id
        self.client = httpx.Client(base_url=self.base_url, timeout=30.0)  # synchronous client

    def _get_headers(self):
        return {
            'X-API-Key': self.api_key,
            'X-API-Secret': self.api_secret,
            'X-Tenant-ID': self.tenant_id,
            'Content-Type': 'application/json',
        }

    def get(self, endpoint, params=None):
        response = self.client.get(endpoint, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        response = self.client.post(endpoint, headers=self._get_headers(), json=data)
        response.raise_for_status()
        return response.json()
    
    def get_news(self, page=1, limit=20):
        return self.get('/api/v1/news', params={'page': page, 'limit': limit})

    def get_events(self, start_date=None, end_date=None):
        params = {}
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        return self.get('/api/v1/events', params=params)

