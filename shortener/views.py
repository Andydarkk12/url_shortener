from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import ShortLink

@csrf_exempt
def create_short_link(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Другой метод'}, status=405)
    
    try:
        # Получаем данные из запроса
        data = json.loads(request.body)
        original_url = data.get('url')
        
        if not original_url:
            return JsonResponse({'error': 'Url неверный'}, status=400)
        
        short_url = ShortLink.generate_unique_short_url()
        
        link = ShortLink.objects.create(
            original_url=original_url,
            short_url=short_url
        )
        
        return JsonResponse({
            'short_id': link.short_url,
            'short_url': f'/{link.short_url}',
            'original_url': link.original_url
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_stats(request, short_url):
    try:
        link = ShortLink.objects.get(short_url=short_url)
        
        return JsonResponse({
            'short_id': link.short_url,
            'original_url': link.original_url,
            'clicks': link.clicks,
            'created_at': link.created_at,
            'short_url': f'/{link.short_url}'
        })
        
    except ShortLink.DoesNotExist:
        return JsonResponse({'error': 'Ссылка не найдена'}, status=404)


def redirect_to_original(request, short_url):
    try:
        link = ShortLink.objects.get(short_url=short_url)
        
        link.increment_clicks()
        
        return HttpResponseRedirect(link.original_url)
        
    except ShortLink.DoesNotExist:
        return JsonResponse({'error': 'Ссылка не найдена'}, status=404)
