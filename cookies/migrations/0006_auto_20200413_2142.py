# Generated by Django 2.2.10 on 2020-04-13 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookies', '0005_auto_20200411_1344'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statutpagetext',
            options={'verbose_name': 'Statut', 'verbose_name_plural': 'Statut'},
        ),
        migrations.AlterModelOptions(
            name='tospagetext',
            options={'verbose_name_plural': 'Termeni si conditii'},
        ),
    ]
