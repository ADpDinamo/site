from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect, HttpResponseForbidden

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import render

from django.views import View
from django.views.generic import DetailView, RedirectView, UpdateView, TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from cookie_consent.util import get_cookie_value_from_request

from membership.models import UserMembership, Subcription, Membership
from payment.extras import gateway, generate_client_token

from allauth.account.views import SignupView
from .forms import Profile


class CustomSignupView(SignupView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        nonce_token = generate_client_token()
        memberships = Membership.objects.all().order_by('order')
        context['nonce_token'] = nonce_token
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


@login_required
def PaymentView(request):

    payment_method_nonce = request.POST.get('payment_method_nonce')

    if payment_method_nonce:

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

    return reverse('users:detail', kwargs={"username": request.user.username})



class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = 'users/user_detail.html'

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
        current_membership_test = get_user_membership(self.request)

        if self.request.user.is_authenticated:
            current_membership = get_user_membership(self.request)
            context['current_membership'] = str(current_membership.membership)
            print(Profile())
            context['form'] = Profile()

        nonce_token = generate_client_token()
        context['nonce_token'] = nonce_token
        return context


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = Profile
    template_name = 'users/user_detail.html'

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
        current_membership_test = get_user_membership(self.request)

        if self.request.user.is_authenticated:
            current_membership = get_user_membership(self.request)
            context['current_membership'] = str(current_membership.membership)

        nonce_token = generate_client_token()
        context['nonce_token'] = nonce_token
        return context

    def get_initial(self):
        initial = super().get_initial()
        # retrieve current object
        habit_object = self.get_object()
        initial['name'] = habit_object.name
        initial['first_name'] = habit_object.first_name
        initial['last_name'] = habit_object.last_name
        initial['last_name'] = habit_object.last_name
        initial['mobile_number'] = habit_object.mobile_number
        initial['date_of_birth'] = habit_object.date_of_birth
        initial['street1'] = habit_object.street1
        initial['zip_code'] = habit_object.zip_code
        initial['city'] = habit_object.city
        initial['country'] = habit_object.country
        return initial

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


class ProfilSocio(View):
    def get(self, request, *args, **kwargs):
        # view = UserDetailView.as_view()
        view = UserUpdateView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = UserUpdateView.as_view()
        return view(request, *args, **kwargs)


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False
    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
