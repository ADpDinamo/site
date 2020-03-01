from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class User(AbstractUser):

    # Full address
    street1 = CharField(blank=True, max_length=255)
    street2 = CharField(blank=True, max_length=255)
    city = CharField(blank=True, max_length=255)
    county = CharField(blank=True, max_length=255)
    country = CharField(blank=True, max_length=255)
    zip_code = CharField(blank=True, max_length=255)


    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)

    # ---------Mobile phone field ------------------
    # error message when a wrong format entered
    mobile_error_message = 'Phone number must be entered in the format: 05999999999'

    mobile_regex = RegexValidator(
        regex=r'^\d{15}$',
        message=mobile_error_message
    )
    mobile_number = CharField(validators=[mobile_regex], max_length=60,
                             null=True, blank=True)

    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)


    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
