# Generated by Django 4.1.7 on 2023-03-28 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_customer_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
