from django.urls import path, include

urlpatterns = [
    path('product', include('products.urls')),
    path('users', include('users.urls')),
    path('survey', include('surveys.urls')),
    path('orders', include('orders.urls')),
]
