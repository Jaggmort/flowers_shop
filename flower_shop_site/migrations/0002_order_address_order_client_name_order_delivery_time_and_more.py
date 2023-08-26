# Generated by Django 4.2.4 on 2023-08-26 06:31

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('flower_shop_site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Адрес доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='client_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Имя клиента'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_time',
            field=models.CharField(blank=True, choices=[('Как можно скорее', 'Как можно скорее'), ('с 10:00 до 12:00', 'с 10:00 до 12:00'), ('с 12:00 до 14:00', 'с 12:00 до 14:00'), ('с 14:00 до 16:00', 'с 14:00 до 16:00'), ('с 16:00 до 18:00', 'с 16:00 до 18:00'), ('с 18:00 до 20:00', 'с 18:00 до 20:00')], max_length=16, null=True, verbose_name='Предпочитаемое время доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон'),
        ),
        migrations.DeleteModel(
            name='Delivery',
        ),
    ]
