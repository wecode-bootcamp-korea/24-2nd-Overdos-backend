from django.urls import path
from django.urls import path
from .views import CartDeleteAll, CartView, CartProductCheckState

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/cart/check', CartProductCheckState.as_view()),
    path('/cart/flush', CartDeleteAll.as_view()),
]