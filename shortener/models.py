from django.db import models
import random
import string

class ShortLink(models.Model):
    original_url = models.URLField(
        max_length=500,
        verbose_name="Оригинальная ссылка"
    )
    short_url = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        verbose_name="Короткая ссылка"
    )
    clicks = models.IntegerField(
        default=0,
        verbose_name="Количество переходов"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    
    def __str__(self):
        return f"{self.short_url} -> {self.original_url[:30]}..."
    
    def increment_clicks(self):
        self.clicks += 1
        self.save(update_fields=['clicks'])
    
    @classmethod
    def generate_unique_short_url(cls, length=6):
        characters = string.ascii_letters + string.digits
        while True:
            short_url = ''.join(random.choices(characters, k=length))
            if not cls.objects.filter(short_url=short_url).exists():
                return short_url