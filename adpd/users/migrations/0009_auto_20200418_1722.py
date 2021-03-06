# Generated by Django 2.2.10 on 2020-04-18 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200413_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='rol',
            field=models.SmallIntegerField(choices=[(0, 'regular user'), (1, 'admin newsletter'), (2, 'admin blog'), (3, 'admin payment'), (4, 'admin phone'), (5, 'admin postal'), (6, 'administrator')], default=0),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='users.UserRole'),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
