from django.contrib import admin
from django.utils.safestring import mark_safe


from shop.models import (
                            Section,
                            Product,
                            Discount,
                            Order,
                            OrderList,
                            Feedback
                        )
from shop.constants import ROUND_VALUE

admin.site.register(Section)
admin.site.register(Discount)


class PriceFilter(admin.SimpleListFilter):
    """Кастомный фильтр по ценам"""

    title = 'Цена'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        # Внешний вид фильтра
        filters = []
        product = Product.objects.order_by('price').last()
        if product:
            max_price = round(product.price / ROUND_VALUE) * ROUND_VALUE + ROUND_VALUE
            price = ROUND_VALUE
            while price <= max_price:
                start = price
                start_price = price - ROUND_VALUE
                if start_price != 0:
                    start_price += 1
                end = '{0} - {1}'.format(start_price, price)
                filters.append((start, end))
                price += ROUND_VALUE
        return filters

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        value = int(self.value())
        return queryset.filter(
            price__gte=(value - ROUND_VALUE + 1), price__lte=value
        )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'section', 'size', 'price', 'created', 'image_show'
    )
    actions_on_bottom = True
    list_per_page = 10
    search_fields = ('title',)
    list_filter = ('title', PriceFilter,)

    def image_show(self, obj):
        if obj.image:
            return mark_safe(
                "<img src='{}' width='60' />".format(obj.image.url)
            )
        return None
        
    image_show.__name__ = 'Картинка'


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'display_product',
        'display_amount',
        'phone_number',
        'email',
        'address',
        'notice',
        'date_order',
        'status',
    )

    fieldsets = (
        ('Информация о заказе', {
            'fields': ('discount', 'notice',)
        }),
        ('Информация о клиенте', {
            'fields': ('name', 'phone_number', 'email', 'address',)
        }),
        ('Информация о доставке', {
            'fields': ('status',)
        }),
    )

    date_hierarchy = 'date_order'
    list_filter = ('status', 'date_order',)


class OrderListAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'count')


class FeedbackListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'message', 'date_feedback', 'status')
    list_filter = ('status',)
    search_fields = ('id',)


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderList, OrderListAdmin)
admin.site.register(Feedback, FeedbackListAdmin)
