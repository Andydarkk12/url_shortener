from django.urls import path
from . import views

urlpatterns = [
    path('shorten', views.create_short_link, name='create_short_link'),
    
    path('stats/<str:short_url>', views.get_stats, name='get_stats'),
    
    path('<str:short_url>', views.redirect_to_original, name='redirect'),
]