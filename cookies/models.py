from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class CookiePageText(models.Model):
    cookie_text = RichTextField()
    tos_text = RichTextField()
    statut_text = RichTextField()

    class Meta:
        verbose_name = 'Legal'
        verbose_name_plural = 'Legale'
