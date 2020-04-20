from django.conf.urls import url

from .views import CheckoutView, RecievePayment
from users.views import PaymentView


urlpatterns = [
    url(r'^checkout/$', CheckoutView.as_view(),
        name='checkout'),
    url(r'^checkout/recieve/$', PaymentView,
        name='recieve'),
    # url(r'^checkout/recieve/$', RecievePayment.as_view(),
    #     name='recieve'),

]
