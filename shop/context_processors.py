from shop.models import Section, Product


def add_default_data(request):
    sections = Section.objects.all()
    count_in_cart = 0
    summ_in_cart = 0
    cart_info = request.session.get('cart_info', {})
    for key in cart_info:
        count_in_cart += cart_info[key]
        summ_product = Product.objects.get(pk=key).price * cart_info[key]
        summ_in_cart += summ_product
    return {
        'sections': sections,
        'count_in_cart': count_in_cart,
        'summ_in_cart': summ_in_cart,
    }
