# Generated by Django 2.2.10 on 2020-04-18 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0002_membership_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='order',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]