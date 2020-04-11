from django.contrib import admin
from .models import CookiePageText

# Register your models here.
class CookieAdmin(admin.ModelAdmin):
    pass

admin.site.register(CookiePageText, CookieAdmin)
