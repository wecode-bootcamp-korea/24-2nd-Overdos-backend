import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "filling.settings")
django.setup()

from products.models import *

CSV_PATH_PRODUCTS = 'products.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        
        if row[0] != '':
            product_name = row[0]
            
        if row[1] != '':
            product_sub_name = row[1]
            
        if row[2] != '':
            product_price = row[2]
            
        if row[3] != '':
            product_description = row[3]
            
        if row[4] != '':
            product_sub_description = row[4]
            
        if row[5] != '':
            image_url = row[5]
        
        if row[6] != '':
            summary_name = row[6]
        
        if row[7] != '':
            food_name = row[7]
        
        if row[8] != '':
            daily_dose = row[8]
                
        if row [9] != '':
            food_url = row[9]
            
        product = Product.objects.create(
            name = product_name,
            sub_name = product_sub_name,
            price = product_price,
            description = product_description,
            sub_description = product_sub_description
        )
        
        Image.objects.create(image_url = image_url, product = product)
        
        Summary.objects.create(name = summary_name, product = product)
        
        # food_list = food_name.split(',')
        # for food in food_list:
        #     if (not Food.objects.filter(name = food).exists()) and food != '':
        #         fo1 = Food.objects.create(name = food, daily_dose = daily_dose, food_url = food_url)
        #     food.product.add(fo1)
        
        # feature_list = row[10].split(',')
        # for feature in feature_list:
        #     if (not Feature.objects.filter(name = feature).exists()) and feature != '':
        #         f1 = Feature.objects.create(name = feature)
        #     feature.food.add(f1)
            
            
        # product = Product.objects.create(
        #     name          = row[3], 
        #     price         = row[4], 
        #     discount      = row[5], 
        #     sales_unit    = row[6], 
        #     weight        = row[7], 
        #     shipping_type = row[8], 
        #     origin        = row[9], 
        #     package_type  = row[10], 
        #     infomation    = row[11], 
        #     sub_category  = sub_category)

        # ProductImage.objects.create(product = product, image_url = row[12])
        
        # allergy_list = row[13].split(',')
        # for allergy in allergy_list:
        #     if (not Allergy.objects.filter(name = allergy).exists()) and allergy != '':
        #         al = Allergy.objects.create(name = allergy)
        #         product.allergy.add(al)
                
                
        

            


 