# Generated by Django 2.2.10 on 2020-04-11 13:41

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookies', '0002_auto_20200411_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusPageText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_text', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='TOSPageText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tos_text', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='cookiepagetext',
            options={'verbose_name': 'Legal', 'verbose_name_plural': 'Legale'},
        ),
        migrations.RemoveField(
            model_name='cookiepagetext',
            name='statut_text',
        ),
        migrations.RemoveField(
            model_name='cookiepagetext',
            name='tos_text',
        ),
    ]
