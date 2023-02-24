from django.urls import path

from shop import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
    path('add_order/', views.add_order, name='add_order'),
    path('reviews/', views.reviews, name='reviews'),
    path('add_review/', views.ReviewCreate.as_view(), name='add_review'),
]
