import json
import bcrypt
import jwt

from django.test import TestCase, Client
from .models import Cart
from products.models import Product, Image
from users.models import User
from my_settings import ALGORITHM, SECRET_KEY

from users.utils import user_auth

class CartViewTest(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('Abcd123!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        u1 = User.objects.create(
            id = 1,
            name = 'Owen',
            email = 'apple@gmail.com',
            password = hashed_password,
            phone_number = '01011110000',
            social_id = 1
        )
        
        u2 = User.objects.create(
            id = 2,
            name = 'Chris',
            email = 'orange@gmail.com',
            password = hashed_password,
            phone_number = '01011112222',
            social_id = 2
        )
        
        p1 = Product.objects.create(
                id = 1,
                name = 'Vitamin C',
                sub_name = 'delicious',
                price = 19000,
                description = 'Expensive and luxurious',
                sub_description = 'Health, stress, skin improvement'
        )
        
        Image.objects.create(image_url = 'www.abc.html', product = p1)
        
        Cart.objects.create(quantity = 1, checkbox = True, user = u1, product = p1)
        
    def tearDown(self):
        Cart.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()
    
    def test_cart_view_post_add_products_in_cart_success(self):
        client = Client()
        
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = ALGORITHM)
        
        header = {'HTTP_Authorization' : access_token}
        response = client.post(
            '/orders/cart', 
            content_type='application/json', 
            **header,
            data=json.dumps({
                'product_id': 1,
                'quantity'  : 1
            })
        )
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'SUCCESS, PRODUCT ADDED TO CART'})

    def test_cart_view_post_product_does_not_exist(self):
        client = Client()
        
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = ALGORITHM)
        
        header = {'HTTP_Authorization' : access_token}
        response = client.post(
            '/orders/cart',
            content_type = 'applicationn/json',
            **header,
            data = json.dumps({
            'product_id' : 5,
            'quantity'   : 1
            })
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'PRODUCT DOES NOT EXIST'})

    def test_cart_view_post_key_error(self):
        client = Client()
        
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = ALGORITHM)
        
        header = {'HTTP_Authorization' : access_token}
        response = client.post(
            '/orders/cart',
            content_type = 'applicationn/json',
            **header,
            data = json.dumps({
            'product_idddddd' : 1,
            'quantity'        : 1
            })
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})

    
    def test_cart_view_put_add_quantity_product_cart_success(self):
        client = Client()
        
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = ALGORITHM)
        
        header = {'HTTP_Authorization' : access_token}
        response = client.put(
            '/orders/cart',
            content_type = 'applicationn/json',
            **header,
            data = json.dumps({
            'product_id' : 1,
            'quantity'   : 2
            })
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'QUANTITY UPDATED SUCCESSFULLY'})
    
    def test_cart_view_put_remove_quantity_product_cart(self):
        client = Client()
        
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = ALGORITHM)
        
        header = {'HTTP_Authorization' : access_token}
        response = client.put(
            '/orders/cart',
            content_type = 'applicationn/json',
            **header,
            data = json.dumps({
            'product_id' : 1,
            'quantity'   : 3
            })
        )
        
        response = client.put(
            '/orders/cart',
            content_type = 'applicationn/json',
            **header,
            data = json.dumps({
            'product_id' : 1,
            'quantity'   : 2
            })
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'QUANTITY UPDATED SUCCESSFULLY'})
    
    def test_cart_view_put_update_quantity_key_error(self):
        client = Client()
        
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = ALGORITHM)
        
        header = {'HTTP_Authorization' : access_token}
        response = client.put(
            '/orders/cart',
            content_type = 'applicationn/json',
            **header,
            data = json.dumps({
            'product_idDDD' : 1,
            'quantity'   : 2
            })
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
    
    def test_cart_view_get_products_cart_success(self):
        client = Client()
        
        access_token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = ALGORITHM)
        
        header = {'HTTP_Authorization' : access_token}
        
        response = client.get(
            '/orders/cart',
            content_type = 'application/json',
            **header
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 
            {'products_list': [{
            'id'            : 1,
            'name'          : 'Vitamin C',
            'product_id'    : 1,
            'product_image' : 'www.abc.html',
            'price'         : 19000,
            'quantity'      : 1,
            'checked'       : 1
            }]
        })
    
    def test_cart_view_get_cart_is_empty(self):
        client = Client()
        
        access_token = jwt.encode({'id' : 2}, SECRET_KEY, algorithm = ALGORITHM)
        
        header = {'HTTP_Authorization' : access_token}
        
        response = client.get(
            '/orders/cart',
            content_type = 'application/json',
            **header
        )
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.json(), {'message' : 'CART IS EMPTY'})
    
#     def test_cart_view_delete_selected_products_cart_success(self):
#         pass
    
#     def test_cart_view_delete_no_products_to_delete(self):
#         pass
    
#     def test_cart_view_delete_key_error(self):
#         pass
    
    
# class CartDeleteAllTest(TestCase):
#     def setUp(self):
#         pass
    
#     def tearDown(self):
#         pass
    
#     def test_cart_delete_all_success(self):
#         pass
    
#     def test_delete_when_cart_is_empty(self):
#         pass
    
#     def test_cart_delete_key_error(self):
#         pass
    
        
    


