from django.contrib import admin
from .models import CookiePageText, TOSPageText, StatutPageText

# Register your models here.
class CookieAdmin(admin.ModelAdmin):
    pass
class TOSPageTextAdmin(admin.ModelAdmin):
    pass
class StatutPageTextAdmin(admin.ModelAdmin):
    pass

admin.site.register(CookiePageText, CookieAdmin)
admin.site.register(TOSPageText, TOSPageTextAdmin)
admin.site.register(StatutPageText, StatutPageTextAdmin)
