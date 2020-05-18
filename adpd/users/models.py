from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, BooleanField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class UserRole(models.Model):
    ROLE_CHOICES = (
        (0, 'regular user'),
        (1, 'admin newsletter'),
        (2, 'admin blog'),
        (3, 'admin payment'),
        (4, 'admin phone'),
        (5, 'admin postal'),
        (6, 'administrator')
    )

    rol = models.SmallIntegerField(choices=ROLE_CHOICES)

    def __str__(self):
        return self.get_rol_display()

class User(AbstractUser):

    # Full address
    street1 = CharField(blank=True, max_length=255)
    street2 = CharField(blank=True, max_length=255)
    city = CharField(blank=True, max_length=255)
    county = CharField(blank=True, max_length=255)
    country = CharField(blank=True, max_length=255)
    zip_code = CharField(blank=True, max_length=255)
    member = CharField(blank=False, max_length=20, null=True)
    tos = BooleanField()


    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=30)

    # ---------Mobile phone field ------------------
    # error message when a wrong format entered
    mobile_error_message = 'Introdu doar cifre.'

    mobile_regex = RegexValidator(
        regex=r'^\d{9,15}$',
        message=mobile_error_message
    )
    mobile_number = CharField(validators=[mobile_regex], max_length=15,
                             null=True, blank=True)

    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)

    # roles = models.ForeignKey(UserRole, on_delete=models.CASCADE, default=0)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
