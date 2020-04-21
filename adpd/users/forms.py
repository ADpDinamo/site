from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Button, Submit, ButtonHolder
# from crispy_forms.bootstrap import TabHolder, Tab, Div, Field, StrictButton

from django import forms as f

from allauth.account.forms import SignupForm
from membership.models import Membership

User = get_user_model()

class MyCustomSignupForm(SignupForm):
    member = f.CharField(required=True)
    tos = f.BooleanField(required=True)
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'POST'
    #     self.helper.form_id = 'id-exampleForm'
    #     self.helper.layout = Layout(
    #         TabHolder(
    #             Tab('Profil',
    #                 'username', 'email', 'password1', 'password2',
    #                 Button('Next', 'Next', css_class="btnNext")
    #             ),
    #             Tab('Plata',
    #                 'first_name', 'last_name',
    #                 Button('Previous', 'Previous', css_class="btnPrevious"),
    #             )
    #         )
    #     )
    #     self.helper.layout.append(Submit('submit', 'Submit'))

    # first_name = f.CharField(required=True)
    # last_name = f.CharField(required=True)
    # street1 = f.CharField(required=True)
    # city = f.CharField(required=True)
    # country = f.CharField(required=True)
    # zip_code = f.CharField(required=True)
    # mobile_number = f.CharField(required=False)
    # date_of_birth = f.DateField(required=True)



class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("De aici? serios? This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])
