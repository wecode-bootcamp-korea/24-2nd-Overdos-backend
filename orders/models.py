from products.models import Product
from users.models    import User
from django.db       import models

class Cart(models.Model):
    quantity = models.IntegerField()
    checkbox = models.BooleanField(default=True)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table='carts'

class Order(models.Model):
    address = models.CharField(max_length=1000)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table='orders'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cart  = models.ForeignKey(Cart, on_delete=models.CASCADE)

    class Meta:
        db_table='orderitems'