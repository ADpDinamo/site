from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.
class CookiePageText(models.Model):
    cookie_text = RichTextField()

    def get_absolute_url(self):
        return reverse('cookie_update')

    class Meta:
        verbose_name = 'Cookie'
        verbose_name_plural = 'Cookie-uri'

class TOSPageText(models.Model):
    tos_text = RichTextField()

    def get_absolute_url(self):
        return reverse('tos_update')

    class Meta:
        verbose_name_plural = 'Termeni si conditii'

class StatutPageText(models.Model):
    statut_text = RichTextField()

    def get_absolute_url(self):
        return reverse('statut_update')

    class Meta:
        verbose_name = 'Statut'
        verbose_name_plural = 'Statut'
