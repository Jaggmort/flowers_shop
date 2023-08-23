from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import post_save


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

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'


class Order(models.Model):
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
    is_payed = models.BooleanField(
        verbose_name='Оплачен',
        default=False
    )

    def __str__(self) -> str:
        return f'{self.created_at.strftime("%Y-%m-%d %H:%M")} - \
            {self.bouquet}: {self.bouquet.price} руб.'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['created_at']


class Delivery(models.Model):
    PREFERRED_DELIVERY_TIME = [
        ('Как можно скорее', 'Как можно скорее'),
        ('с 10:00 до 12:00', 'с 10:00 до 12:00'),
        ('с 12:00 до 14:00', 'с 12:00 до 14:00'),
        ('с 14:00 до 16:00', 'с 14:00 до 16:00'),
        ('с 16:00 до 18:00', 'с 16:00 до 18:00'),
        ('с 18:00 до 20:00', 'с 18:00 до 20:00'),
    ]
    order = models.ForeignKey(
        to=Order,
        verbose_name='Заказ для доставки',
        related_name='order',
        on_delete=models.RESTRICT
    )
    client_name = models.CharField(
        verbose_name='Имя клиента',
        max_length=200
    )
    phone_number = PhoneNumberField(
        verbose_name='Телефон'
    )
    delivery_time = models.CharField(
        verbose_name='Предпочитаемое время доставки',
        choices=PREFERRED_DELIVERY_TIME,
        max_length=16
    )
    address = models.TextField(
        verbose_name='Адрес доставки'
    )

    def __str__(self) -> str:
        return f'Доставка {self.order}, {self.delivery_time}\
            телефон: {self.phone_number}, адрес: {self.address}'

    class Meta:
        verbose_name = 'Заказ на доставку'
        verbose_name_plural = 'Заказы на доставку'


@receiver(post_save, sender=Delivery)
def report_courier(sender, created, instance, **kwargs):
    print('Новый Заказ')
    pass
    # послать сообщение курьеру


class Consultation(models.Model):
    client_name = models.CharField(
        verbose_name='Имя клиента',
        max_length=200
    )
    phone_number = PhoneNumberField(
        verbose_name='Телефон'
    )

    def __str__(self) -> str:
        return f'Требуется консультация {self.client_name},\
            телефон: {self.phone_number}'

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'


@receiver(post_save, sender=Consultation)
def report_consultant(sender, created, instance, **kwargs):
    print('Новая консультация')
    pass
    # послать сообщение консультанту
