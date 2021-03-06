from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views


from adpd.users.views import HomePageView, CustomSignupView
# from adpd.cookies.urls

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("utilizator/", include("adpd.users.urls", namespace="users")),
    path("cont/", include("allauth.urls")),
    path("inregistrare/", CustomSignupView.as_view(), name='reg'),

    # Legal stuff
    path('legale/', include('cookies.urls')),

    # Frontend Admin
    # path('dashboard', )

    # Plati
    path('plata/', include('payment.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
