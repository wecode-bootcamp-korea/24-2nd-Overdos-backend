from core.models import TimeStampModel
from users.models    import User
from products.models import Product
from django.db       import models

class SurveyInfo(TimeStampModel):
    GENDER_CHOICES = (
        ('male','남자'),
        ('female','여자')
    )
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    age    = models.IntegerField()
    user   = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table='surveyinfos'

class Body(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table='bodies'

class Symptom(models.Model):
    description = models.CharField(max_length=200)
    body        = models.ForeignKey(Body,on_delete=models.CASCADE)
    product     = models.ManyToManyField(Product, through='Product_Symptom')
    surveyinfo  = models.ManyToManyField(SurveyInfo, through='SurveyInfo_Symptom')

    class Meta:
        db_table='symptoms'
    
class Product_Symptom(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)

    class Meta:
        db_table='product_symptoms'

class SurveyInfo_Symptom(models.Model):
    surveyinfo = models.ForeignKey(SurveyInfo, on_delete=models.CASCADE)
    symptom    = models.ForeignKey(Symptom, on_delete=models.CASCADE)

    class Meta:
        db_table='surveyinfo_symptoms'