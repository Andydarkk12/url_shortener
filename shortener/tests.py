from django.test import TestCase
from django.urls import reverse
from .models import ShortLink
import json

class ShortLinkModelTests(TestCase):
    
    def test_generate_unique_short_url_length(self):
        short_url = ShortLink.generate_unique_short_url(length=6)
        self.assertEqual(len(short_url), 6)
    
    def test_generate_unique_short_url_unique(self):
        url1 = ShortLink.generate_unique_short_url()
        url2 = ShortLink.generate_unique_short_url()
        self.assertNotEqual(url1, url2)
    
    def test_increment_clicks(self):
        link = ShortLink.objects.create(
            original_url='https://google.com',
            short_url='test123'
        )
        self.assertEqual(link.clicks, 0)
        
        link.increment_clicks()
        self.assertEqual(link.clicks, 1)
        
        link.refresh_from_db()
        self.assertEqual(link.clicks, 1)


class ShortLinkAPITests(TestCase):
    
    def setUp(self):
        self.test_link = ShortLink.objects.create(
            original_url='https://yandex.ru',
            short_url='test123'
        )
    
    def test_create_short_link_success(self):
        response = self.client.post('/api/shorten', 
            data=json.dumps({'url': 'https://google.com'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('short_id', data)
        self.assertIn('short_url', data)
        self.assertEqual(data['original_url'], 'https://google.com')
    
    def test_create_short_link_no_url(self):
        response = self.client.post('/api/shorten',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_get_stats_existing(self):
        response = self.client.get(f'/api/stats/test123')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['short_id'], 'test123')
        self.assertEqual(data['clicks'], 0)
    
    def test_get_stats_not_found(self):
        response = self.client.get('/api/stats/notexists')
        self.assertEqual(response.status_code, 404)
    
    def test_redirect_success(self):
        response = self.client.get('/test123')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://yandex.ru')
        
        self.test_link.refresh_from_db()
        self.assertEqual(self.test_link.clicks, 1)