from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shortener.urls')),      # ЭТО ЕСТЬ?
    path('', include('shortener.urls')),          # ЭТО ЕСТЬ?
]
