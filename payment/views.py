from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.http import HttpResponse, HttpResponseRedirect

from .extras import gateway, transact


# Create your views here.
class CheckoutView(TemplateView):
    template_name = "payment/checkout.html"

    def generate_client_token(self):
        return gateway.client_token.generate()

    # def get(self, request, *args, **kwargs):
    #     # print('self.form', self.form)
    #
    #     print(request)
    #     return render(request, self.template_name)


    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        print(response)

        # if get_cookie_value_from_request(request, "optional") is True:
        #     val = "optional cookie set from django"
        #     response.set_cookie("optional_test_cookie", val)
        # else:
        #     response.delete_cookie("optional_test_cookie")

        return response



    def post(self, request, *args, **kwargs):
        print('self.form', self.form)
        print(request)
        response = request.form['payment_method_nonce']
        # return HttpResponse(response)
        return HttpResponseRedirect(reverse('recieve', kwargs={'payment_method_nonce':request.form['payment_method_nonce']}))


class RecievePayment(TemplateView):
    template_name = "payment/recieve.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        print('response-get', response)
        print('self-get', self.__dir__())
        print('self-request-get', self.request)
        print('self-request-get', self.request.__dir__())
        print('request-get', request)
        print('kwargs-get', kwargs)
        return response

    def post(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        print('response-post', response)
        print('self', self)
        print('request', request)

        # if get_cookie_value_from_request(request, "optional") is True:
        #     val = "optional cookie set from django"
        #     response.set_cookie("optional_test_cookie", val)
        # else:
        #     response.delete_cookie("optional_test_cookie")

        return response

    # def post(self, request, *args, **kwargs):
    #     print('self', self)
    #     print('request', request)
    #     print('kwargs', kwargs)
    #     return reverse('checkout')

    # result = transact({
    #     'amount': request.form['amount'],
    #     'payment_method_nonce': request.form['payment_method_nonce'],
    #     'options': {
    #         "submit_for_settlement": True
    #     }
    # })
