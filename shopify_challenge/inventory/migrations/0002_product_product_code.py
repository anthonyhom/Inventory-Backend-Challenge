# Generated by Django 3.2.11 on 2022-01-19 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_code',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
