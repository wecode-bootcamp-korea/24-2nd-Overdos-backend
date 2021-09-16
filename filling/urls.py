from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('product', include('products.urls')),
]
