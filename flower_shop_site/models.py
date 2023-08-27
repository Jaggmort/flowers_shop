from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .notifications_bot import send_notification, unify_phone
from django.urls import reverse
from django.template.defaultfilters import slugify


class Tag(models.Model):
    title = models.CharField(
        verbose_name='Тег',
        max_length=25
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Bouquet(models.Model):
    title = models.CharField(
        verbose_name='Название букета',
        max_length=50
    )
    composition = models.TextField(
        verbose_name='Состав букета'
    )
    size = models.TextField(
        verbose_name='Размер букета',
        default='Высота - 50 см\nШирина - 30 см'
    )
    price = models.DecimalField(
        verbose_name='Цена букета',
        max_digits=4,
        decimal_places=0
    )
    image = models.ImageField(
        verbose_name='Фото букета',
        upload_to='bouquet_images/',
        null=True, blank=True
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name='tags',
        verbose_name='Тег',
        blank=True
    )
    slug = models.SlugField(
        verbose_name='Название в виде url',
        max_length=200,
        null=True,
        unique=True
    )
    def get_absolute_url(self):
        return reverse('bouquet_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'


class Order(models.Model):
    PREFERRED_DELIVERY_TIME = [
        ('Как можно скорее', 'Как можно скорее'),
        ('с 10:00 до 12:00', 'с 10:00 до 12:00'),
        ('с 12:00 до 14:00', 'с 12:00 до 14:00'),
        ('с 14:00 до 16:00', 'с 14:00 до 16:00'),
        ('с 16:00 до 18:00', 'с 16:00 до 18:00'),
        ('с 18:00 до 20:00', 'с 18:00 до 20:00'),
    ]
    created_at = models.DateTimeField(
        verbose_name='Время создания заказа',
        default=timezone.now,
        editable=False
    )
    bouquet = models.ForeignKey(
        to=Bouquet,
        verbose_name='Заказанный букет',
        related_name='bouquet',
        on_delete=models.RESTRICT
    )
    client_name = models.CharField(
        verbose_name='Имя клиента',
        max_length=200,
        null=True, blank=True
    )
    phone_number = PhoneNumberField(
        verbose_name='Телефон',
        null=True, blank=True
    )
    delivery_time = models.CharField(
        verbose_name='Предпочитаемое время доставки',
        choices=PREFERRED_DELIVERY_TIME,
        max_length=16,
        null=True, blank=True
    )
    address = models.TextField(
        verbose_name='Адрес доставки',
        null=True, blank=True
    )
    is_payed = models.BooleanField(
        verbose_name='Оплачен',
        default=False
    )
    is_notification_sent = models.BooleanField(
        verbose_name='Отправлено сообщение курьеру',
        default=False
    )

    def __str__(self) -> str:
        return f'{self.created_at.strftime("%Y-%m-%d %H:%M")} - \
            {self.bouquet}: {self.bouquet.price} руб.'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['created_at']


@receiver(post_save, sender=Order)
def report_courier(sender, created, instance, **kwargs):
    if instance.is_payed and instance.is_notification_sent == False:
        message = '*Новый заказ!*\n'\
                 f'Букет: {instance.bouquet}\n'\
                 f'Имя клиента: {instance.client_name}\n'\
                 f'Телефон: `{unify_phone(instance.phone_number)}`\n'\
                 f'Предпочитаемое время доставки:\n*{instance.delivery_time}*\n'\
                 f'Адрес: `{instance.address}`'
        send_notification(
            settings.COURIER_TG_ID,
            message
        )
        instance.is_notification_sent = True
        instance.save()
    # послать сообщение курьеру


class Consultation(models.Model):
    client_name = models.CharField(
        verbose_name='Имя клиента',
        max_length=200
    )
    phone_number = PhoneNumberField(
        verbose_name='Телефон'
    )
    is_notification_sent = models.BooleanField(
        verbose_name='Отправлено сообщение консультанту',
        default=False
    )

    def __str__(self) -> str:
        return f'Требуется консультация {self.client_name},\
            телефон: {self.phone_number}'

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'


@receiver(post_save, sender=Consultation)
def report_consultant(sender, created, instance, **kwargs):
    if instance.is_notification_sent == False:
        message = '*Запрос на консультацию!*\n'\
                f'Имя клиента: *{instance.client_name}*\n'\
                f'Телефон: `{unify_phone(instance.phone_number)}`'
        send_notification(
            settings.CONSULTANT_TG_IG,
            message
        )
        instance.is_notification_sent = True
        instance.save()
    # послать сообщение консультанту
