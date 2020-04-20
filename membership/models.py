from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from payment.extras import gateway

MEMBERSHIP_CHOICES = (
    ('Adult', 'AD'),
    ('Senior', 'SR'),
    ('Junior', 'JR')
)

class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES,
        default='Adult',
        max_length=30)
    price = models.IntegerField(default=400)
    gateway_plan = models.CharField(max_length=40)
    description = models.TextField()
    order = models.SmallIntegerField()

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    membru = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gateway_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.membru.email


def post_save_usermembership_create(sender, instance, created, *args, **kwargs):
    if created:
        UserMembership.objects.get_or_create(membru=instance)

    member_of = None
    selected_membership_qs = Membership.objects.filter(
                                        membership_type=instance.member)

    if selected_membership_qs.exists():
        member_of = selected_membership_qs.first()

    user_membership, created = UserMembership.objects.get_or_create(membru=instance)

    if user_membership.gateway_customer_id is None or user_membership.gateway_customer_id == '':
        new_customer_id = gateway.customer.create({"first_name": instance.first_name,
                                                   "last_name": instance.last_name,
                                                   "email": instance.email})
        user_membership.gateway_customer_id = new_customer_id.customer.id
        user_membership.membership = member_of

        user_membership.save()

post_save.connect(post_save_usermembership_create, sender=settings.AUTH_USER_MODEL)


class Subcription(models.Model):
    user_memebership = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    gateway_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.gateway_subscription_id
