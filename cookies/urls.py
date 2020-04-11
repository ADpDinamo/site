# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from cookie_consent.views import (
    CookieGroupListView,
    CookieGroupAcceptView,
    CookieGroupDeclineView,
)

from .views import CookiePageTextListView, TOSListView, StatutListView

urlpatterns = [
    url(r'^cookie/accept/$',
        csrf_exempt(CookieGroupAcceptView.as_view()),
        name='cookie_consent_accept_all'),
    url(r'^cookie/accept/(?P<varname>.*)/$',
        csrf_exempt(CookieGroupAcceptView.as_view()),
        name='cookie_consent_accept'),
    url(r'^cookie/decline/(?P<varname>.*)/$',
        csrf_exempt(CookieGroupDeclineView.as_view()),
        name='cookie_consent_decline'),
    url(r'^cookie/decline/$',
        csrf_exempt(CookieGroupDeclineView.as_view()),
        name='cookie_consent_decline_all'),
    url(r'^cookie/$',
        CookiePageTextListView.as_view(),
        name='cookie_consent_cookie_group_list'),
    url(r'^tos/$',
        TOSListView.as_view(),
        name='tos'),
    url(r'^statut/$',
        StatutListView.as_view(),
        name='statut'),
]
