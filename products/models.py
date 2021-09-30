from users.models import User
from django.db   import models
from core.models import TimeStampModel

class Product(TimeStampModel):
    name            = models.CharField(max_length=40)
    sub_name        = models.CharField(max_length=40)
    price           = models.IntegerField()
    description     = models.CharField(max_length=1000)
    sub_description = models.CharField(max_length=100)
    
    class Meta:
        db_table='products'

class Image(models.Model):
    image_url     = models.URLField(max_length=1000)
    product       = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table='images'

class Summary(models.Model):
    name    = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table='summaries'

class CustomerReview(TimeStampModel):
    review_image_url = models.URLField(max_length=1000)
    review           = models.TextField()
    user             = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table='customerreviews'

class Food(models.Model):
    name       = models.CharField(max_length=40)
    daily_dose = models.CharField(max_length=40)
    food_url   = models.URLField(max_length=1000, default='')
    product    = models.ManyToManyField(Product, through='ProductFood')

    class Meta:
        db_table='foods'

class ProductFood(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    food    = models.ForeignKey(Food, on_delete=models.CASCADE)

    class Meta:
        db_table='product_foods'

class Feature(models.Model):
    name = models.CharField(max_length=100)
    food = models.ManyToManyField(Food, through='FoodFeature')
    
    class Meta:
        db_table='features'

class FoodFeature(models.Model):
    food    = models.ForeignKey(Food, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    class Meta:
        db_table='food_features'
