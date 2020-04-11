from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from cookie_consent.models import CookieGroup
from .models import CookiePageText, TOSPageText, StatutPageText
# Create your views here.


class CookiePageTextListView(ListView):
    model = CookieGroup
    template_name = 'cookie_consent/cookiegroup_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cookie_text = CookiePageText
        context['cookie_text'] = cookie_text.objects.all()
        return context

class CookieTextUpdateView(UpdateView):
    model = CookiePageText
    fields = '__all__'
    template_name = 'cookie_consent/cookie_update.html'

    def get_object(self):
        return CookiePageText.objects.get(pk=1)


class TOSListView(ListView):
    model = TOSPageText
    template_name = 'cookie_consent/tos.html'

class TOSUpdateView(LoginRequiredMixin, UpdateView):
    model = TOSPageText
    fields = '__all__'
    template_name = 'cookie_consent/tos_update.html'

    def get_object(self):
        return TOSPageText.objects.get(pk=1)

class StatutListView(ListView):
    model = StatutPageText
    template_name = 'cookie_consent/statut.html'


class StatutUpdateView(LoginRequiredMixin, UpdateView):
    model = StatutPageText
    fields = '__all__'
    template_name = 'cookie_consent/statut_update.html'

    def get_object(self):
        return StatutPageText.objects.get(pk=1)
