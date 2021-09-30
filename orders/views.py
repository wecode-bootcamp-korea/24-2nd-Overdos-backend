import json

from django.shortcuts import render

from django.views import View
from django.http import JsonResponse

from orders.models import Cart
from products.models import Product
from users.utils import user_auth

class CartView(View):
    @user_auth
    def post(self, request):
        try:
            user_id    = request.user
            data       = json.loads(request.body)
            product_id = data['product_id']
            quantity   = data['quantity']
            
            if not Product.objects.filter(id = product_id).exists():
                return JsonResponse({'message' : 'PRODUCT DOES NOT EXIST'}, status = 400)
            
            if not Cart.objects.filter(user_id = user_id, product_id = product_id,).exists():
                Cart.objects.create(
                    user_id    = request.user,
                    product_id = product_id,
                    quantity   = quantity
                )
            
            return JsonResponse({'message' : 'SUCCESS, PRODUCT ADDED TO CART'}, status = 201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
    
    @user_auth
    def put(self, request):
        try:
            user_id    = request.user
            data       = json.loads(request.body)
            print("ss")
            product_id = data['product_id']
            quantity   = data['quantity']
            
            if Cart.objects.filter(user_id = user_id, product_id = product_id).exists():
                product_in_cart          = Cart.objects.get(user_id = user_id, product_id = product_id)
                product_in_cart.quantity = quantity
                product_in_cart.save()
                
            return JsonResponse({'message' : 'QUANTITY UPDATED SUCCESSFULLY'}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
    @user_auth
    def get(self, request):
        user_id = request.user
        carts   = Cart.objects.filter(user_id = user_id)
        
        if not carts.exists():
            return JsonResponse({'message' : 'CART IS EMPTY'}, status = 204)
        
        return JsonResponse({'products_list' : 
            [{
            'id'            : user_id,
            'name'          : cart.product.name,
            'product_id'    : cart.product.id,
            'product_image' : cart.product.image_set.first().image_url,
            'price'         : cart.product.price,
            'quantity'      : cart.quantity,
            'checked'       : cart.checkbox
        } for cart in carts]}, status = 201)
        
        
class CartProductCheckState(View):
    @user_auth
    def put(self, request):
        try:
            user_id    = request.user
            data       = json.loads(request.body)
            
            product_id = data['product_id']
            quantity   = data['quantity']
            checked    = data['checked']
            
            print(f"checked variable :: {type(checked)}")
            print(f"checked variable :: {type(checked)}")
            print(f"checked variable :: {type(checked)}")

            if Cart.objects.filter(user_id = user_id, product_id = product_id).exists():
                product_in_cart          = Cart.objects.get(user_id = user_id, product_id = product_id)
                product_in_cart.quantity = quantity
                product_in_cart.checkbox = checked
                product_in_cart.save()
                
            return JsonResponse({'message' : 'PRODUCT CHECKED SUCCESS'}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        
class CartDeleteAll(View):
    @user_auth
    def delete(self, request):
        try:
            user_id = request.user
            
            products_in_cart = Cart.objects.filter(user_id = user_id)
            
            if not products_in_cart.exists():
                return JsonResponse({'message' : 'NO PRODUCTS TO DELETE'}, status =400)
            
            products_in_cart.delete()
            return JsonResponse({'message' : 'DELETED SUCCESSFULLY'}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
