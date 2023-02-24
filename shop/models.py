from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


from shop.constants import (
                            STATUSES_ORDER,
                            STATUSES_OF_THE_REQUEST,
                            )


class Section(models.Model):
    """Модель разделов"""

    title = models.CharField(
        max_length=70,
        help_text='Название раздела',
        unique=True,
        verbose_name='Название раздела',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.title


class Product(models.Model):
    """Модель продукта"""

    section = models.ForeignKey(
        Section,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Раздел'
    )
    title = models.CharField(max_length=100, verbose_name='Название продукта')
    image = models.ImageField(upload_to='images', verbose_name='Изображение')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name='Цена'
    )
    size = models.CharField(max_length=3, verbose_name='Размер')
    description = models.TextField(verbose_name='Описание')
    available = models.BooleanField(
        default=True,
        verbose_name='Наличие продукта'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания продукта'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Время последнего обновления'
    )

    count = 1

    class Meta:
        ordering = ['title']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_count(self):
        return self.count

    def get_summ_price(self):
        return self.count * self.price

    def __str__(self):
        return f'{self.title} ({self.section.title})'


class Discount(models.Model):
    """Модель скидки"""

    code = models.CharField(max_length=10, verbose_name='Код купона')
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Размер скидки',
        help_text='В процентах'
    )

    class Meta:
        ordering = ['-value']
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return f'{self.code} ({self.value}%)'


class Order(models.Model):
    """Модель заказа продукта"""

    discount = models.ForeignKey(
        'Discount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Скидка'
    )
    name = models.CharField(max_length=70, verbose_name='Имя')
    phone_number = models.CharField(
        max_length=70,
        verbose_name='Номер телефона'
    )
    email = models.EmailField(blank=True)
    address = models.TextField(verbose_name='Адрес доставки')
    notice = models.TextField(blank=True, verbose_name='Примечания к заказу')
    date_order = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата заказа'
    )
    status = models.CharField(
        choices=STATUSES_ORDER,
        max_length=3,
        default='NEW',
        verbose_name='Статус заказа'
    )

    class Meta:
        ordering = ['-date_order']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def display_product(self):
        display = ''
        for order_line in self.orderlist_set.all():
            display += '{0}, {1} см: {2} шт.; '.format(
                order_line.product.title,
                order_line.product.size,
                order_line.count
            )
        return display

    def display_amount(self):
        amount = 0
        for order_line in self.orderlist_set.all():
            amount += order_line.price * order_line.count

        if self.discount:
            amount = round(amount * Decimal(1 - self.discount.value / 100))
        return f'{amount} руб.'

    def __str__(self):
        return f'ID: ({self.id})'

    display_product.short_description = 'Состав заказа'
    display_amount.short_description = 'Сумма заказа'


class OrderList(models.Model):
    """Модель строки заказа"""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Товар'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Цена'
    )
    count = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Строка заказа'
        verbose_name_plural = 'Строки заказов'

    def __str__(self):
        return (
            f'Заказ (ID {self.order.id}) '
            f'{self.product.title}: {self.count} шт.'
        )


class Feedback(models.Model):
    """Модель обратной связи"""

    name = models.CharField(max_length=70, verbose_name='Имя')
    email = models.EmailField()
    message = models.TextField(blank=True, verbose_name='Сообщение')
    date_feedback = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата обращения'
    )
    status = models.CharField(
        choices=STATUSES_OF_THE_REQUEST,
        max_length=3,
        default='NPR',
        verbose_name='Статус заказа'
    )

    class Meta:
        ordering = ['-date_feedback']
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'

    def __str__(self):
        return (
            f'Обращение {self.id}, {self.date_feedback}: '
            f'от {self.name} - {self.message}'
        )


class Reviews(models.Model):
    """Отзывы"""

    email = models.EmailField(blank=True)
    name = models.CharField(max_length=70, blank=True, verbose_name='Имя')
    message = models.TextField(verbose_name='Сообщение')
    date_review = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )

    class Meta:
        ordering = ['-date_review']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return (
            f'Отзыв {self.id}, {self.date_review}: '
            f'от {self.name} - {self.message}'
        )
