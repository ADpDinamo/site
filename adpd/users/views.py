from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render

from django.http import HttpResponseRedirect

from django.views.generic import DetailView, RedirectView, UpdateView, TemplateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from cookie_consent.util import get_cookie_value_from_request

from membership.models import UserMembership, Subcription, Membership
from payment.extras import gateway, generate_client_token

from allauth.account.views import SignupView


class CustomSignupView(SignupView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        print(self.request.GET)

        nonce_token = generate_client_token()
        context['nonce_token'] = nonce_token

        memberships = Membership.objects.all().order_by('order')
        context['memberships'] = memberships


        return context

User = get_user_model()


def get_user_membership(request):
    if request.user.is_authenticated:
        user_membership_qs = UserMembership.objects.filter(membru=request.user)
        if user_membership_qs.exists():
            return user_membership_qs.first()
    return None


def get_user_subscription(request):
    user_subscription_qs = Subcription.objects.filter(user_memebership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None


def get_selected_membership(request):

    # membership_type = request.session['selected_membership_type']
    membership_type = request.user.member

    selected_membership_qs = Membership.objects.filter(
                                        membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        memberships = Membership.objects.all().order_by('order')

        context['memberships'] = memberships

        if self.request.user.is_authenticated:
            current_membership = get_user_membership(self.request)
            context['current_membership'] = str(current_membership.membership)

            subscription_qs = get_user_subscription(self.request)
            if subscription_qs:
                subscription = gateway.subscription.find(str(subscription_qs))
                context['subscription'] = subscription
        return context

    # def post(self, request, **kwargs):
    #     selected_membership_type = request.POST.get('membership_type')
    #
    #     print(request.POST)
    #
    #     selected_membership_qs = Membership.objects.filter(
    #         membership_type=selected_membership_type
    #     )
    #
    #     if selected_membership_qs.exists():
    #         selected_membership = selected_membership_qs.first()
    #
    #     # assign to session
    #     request.session['selected_membership_type'] = selected_membership.membership_type
    #
    #     return HttpResponseRedirect(reverse('recieve'))



def PaymentView(request):
    payment_method_nonce = request.POST.get('payment_method_nonce')

    # Tip abonament selectat
    selected_membership = get_selected_membership(request)
    selected_membership_qs = Membership.objects.filter(
                                        membership_type=selected_membership)
    if selected_membership_qs.exists():
        memb =  selected_membership_qs.first()

    # braintree customer ID
    user_membership = get_user_membership(request)

    payment_token = gateway.payment_method.create({
        "customer_id": user_membership.gateway_customer_id,
        "payment_method_nonce": payment_method_nonce
    })

    result = gateway.subscription.create({
        "payment_method_token": payment_token.payment_method.token,
        "plan_id": memb.gateway_plan
    })

    if result.subscription.id and user_membership:
        sub = Subcription.objects.get_or_create(gateway_subscription_id=result.subscription.id, user_memebership=user_membership)

    context = {'selected_membership': selected_membership,
                'subscription': sub}

    return render(request, "payment/recieve.html", context)



class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        memberships = Membership.objects.all().order_by('order')


        subscription_qs = get_user_subscription(self.request)
        if subscription_qs:
            subscription = gateway.subscription.find(str(subscription_qs))
            context['subscription'] = subscription

        # braintree customer ID
        user_membership = get_user_membership(self.request)
        customer = gateway.customer.find(user_membership.gateway_customer_id)
        context['customer'] = customer


        context['memberships'] = memberships

        if self.request.user.is_authenticated:
            current_membership = get_user_membership(self.request)
            context['current_membership'] = str(current_membership.membership)


        nonce_token = generate_client_token()
        context['nonce_token'] = nonce_token
        return context


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name", "mobile_number", "date_of_birth"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
