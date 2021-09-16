from django.urls import path

from products.views import ProductView, ProductDetailView

urlpatterns = [
    path('/list', ProductView.as_view()),
    path('/detail', ProductDetailView.as_view()),
]
