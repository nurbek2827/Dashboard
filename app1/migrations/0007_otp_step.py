# Generated by Django 4.2.1 on 2023-07-24 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='step',
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
    ]
