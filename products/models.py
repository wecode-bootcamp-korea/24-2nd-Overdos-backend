from django.db import models

class Product(models.Model):
    name            = models.CharField(max_length=40)
    sub_name        = models.CharField(max_length=40)
    price           = models.IntegerField()
    description     = models.CharField(max_length=1000)
    sub_description = models.CharField(max_length=100)

    class Meta:
        db_table='products'

class Image(models.Model):
    url     = models.URLField(max_length=1000)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table='images'

class Summary(models.Model):
    name    = models.CharField(max_length=100)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table='summaries'

class CustomerReview(models.Model):
    image_url = models.URLField(max_length=1000)
    review    = models.TextField()
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)
    user      = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table='customerreviews'

class Food(models.Model):
    name       = models.CharField(max_length=40)
    daily_dose = models.CharField(max_length=40)
    product    = models.ManyToManyField('Product',through='ProductFood')

    class Meta:
        db_table='foods'

class ProductFood(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    foood   = models.ForeignKey('Food',on_delete=models.CASCADE)

    class Meta:
        db_table='product_foods'

class Feature(models.Model):
    name = models.CharField(max_length=100)
    food = models.ManyToManyField('Food',through='FoodFeature')
    
    class Meta:
        db_table='features'

class FoodFeature(models.Model):
    food    = models.ForeignKey('Food',on_delete=models.CASCADE)
    feature = models.ForeignKey('Feature',on_delete=models.CASCADE)

    class Meta:
        db_table='food_features'
