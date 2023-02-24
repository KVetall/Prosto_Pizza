from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from shop.forms import OrderModelForm, ReviewsAddForm


from shop.models import (
    Order,
    OrderList,
    Product,
    Reviews
)


def index(request):
    result = pre_render(request)
    if result:
        return result
    products_pizza = Product.objects.all().filter(section_id=1)
    products_drink = Product.objects.all().filter(section_id=3)
    context = {
        'products_pizza': products_pizza,
        'products_drink': products_drink,
    }
    return render(
        request,
        'index.html',
        context=context
    )


def pre_render(request):
    if request.GET.get('add_cart'):
        product_id = request.GET.get('add_cart')
        get_object_or_404(Product, pk=product_id)
        cart_info = request.session.get('cart_info', {})
        count = cart_info.get(product_id, 0)
        count += 1
        cart_info.update({product_id: count})
        request.session['cart_info'] = cart_info


def page404(request, exception):
    return render(request, 'pageerror.html', status=404)


def cart(request):
    result = update_cart_info(request)
    if result:
        return result

    cart_info = request.session.get('cart_info')
    products = []
    if cart_info:
        for product_id in cart_info:
            product = get_object_or_404(Product, pk=product_id)
            product.count = cart_info[product_id]
            products.append(product)
    return render(
        request,
        'cart.html',
        {'products': products},
    )


def update_cart_info(request):
    if request.GET.get('delete_cart'):
        cart_info = request.session.get('cart_info')
        product_id = request.GET.get('delete_cart')
        get_object_or_404(Product, pk=product_id)
        cart_info.pop(product_id)
        request.session['cart_info'] = cart_info
        return HttpResponseRedirect(reverse('cart'))


def order(request):
    cart_info = request.session.get('cart_info')
    if not cart_info:
        raise Http404()
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order_obj = Order()
            order_obj.name = form.cleaned_data['name']
            order_obj.phone_number = form.cleaned_data['phone_number']
            order_obj.email = form.cleaned_data['email']
            order_obj.address = form.cleaned_data['address']
            order_obj.notice = form.cleaned_data['notice']
            order_obj.save()
            add_order_lines(request, order_obj)
            return HttpResponseRedirect(reverse('add_order'))
    else:
        form = OrderModelForm()

    return render(
        request,
        'order.html',
        {'form': form}
    )


def add_order_lines(request, order_obj):
    cart_info = request.session.get('cart_info', {})
    for key in cart_info:
        order_line = OrderList()
        order_line.order = order_obj
        order_line.product = get_object_or_404(Product, pk=key)
        order_line.price = order_line.product.price
        order_line.count = cart_info[key]
        order_line.save()
    del request.session['cart_info']


def add_order(request):
    return render(
        request,
        'addedorder.html'
    )


def reviews(request):
    objects = Reviews.objects.all()
    return render(
        request,
        'reviews.html',
        context={'objects': objects}
    )


class ReviewCreate(View):

    def get(self, request):
        form = ReviewsAddForm()
        context = {'form': form}
        return render(
            request,
            'reviews_add.html',
            context
        )

    def post(self, request):
        form = ReviewsAddForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('reviews')
        return render(
            request,
            'reviews_add.html',
            context={'form': form}
        )
