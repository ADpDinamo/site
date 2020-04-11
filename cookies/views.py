from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import CookiePageText
from cookie_consent.models import CookieGroup
# Create your views here.


class CookiePageTextListView(ListView):
    model = CookieGroup
    template_name = 'cookie_consent/cookiegroup_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cookie_text = CookiePageText
        context['cookie_text'] = cookie_text.objects.all()
        return context

class TOSListView(ListView):
    model = CookiePageText
    template_name = 'cookie_consent/tos.html'

class StatutListView(ListView):
    model = CookiePageText
    template_name = 'cookie_consent/statut.html'
