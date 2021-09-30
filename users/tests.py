import json
import jwt
import bcrypt
import requests

from django.test import TestCase, Client
from unittest.mock import MagicMock, patch 

from .models import User
from my_settings import ALGORITHM, SECRET_KEY

class UserSignupTest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [User(
                id           = 1,
                name         = 'Owen Koh', 
                email        = 'apple123@gmail.com', 
                password     = 'Abcd1111!', 
                phone_number = '01011112222', 
                social_id    = '12345'
            ),
            User(
                id           = 2,
                name         = 'Brand Kim', 
                email        = 'pear123@gmail.com', 
                password     = 'Abcd1111!', 
                phone_number = '01011113333', 
                social_id    = '121212'
            )]
        )
        
    def tearDown(self):
        User.objects.all().delete()
        
    def test_signup_view_post_user_successfully_created(self):
        client = Client()
        
        user = {
            'name'         : 'Sam Kim',
            'email'        : 'grape@gmail.com',
            'password'     : 'Abcd1234!',
            'phone_number' : '01022223333',
            'social_id'    : '1234321'
            }
        
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
                        {
                            'message' : 'CREATED'
                        }
                    )
        
    def test_signup_view_post_invalid_email(self):
        client = Client()
        
        user = {
            'name'         : 'Kimchi Kim',
            'email'        : 'wrong.gmail.com',
            'password'     : 'Abcd1234!',
            'phone_number' : '01011114444',
            'social_id'    : '22222'
            }
        
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                        {
                            'message' : 'INVALID_EMAIL'
                        }
                    )
    
    def test_signup_view_post_invalid_password(self):
        client = Client()
        
        user = {
            'name'         : 'banana Kim',
            'email'        : 'banana@gmail.com',
            'password'     : 'bcd12!',
            'phone_number' : '01011115555',
            'social_id'    : '22222'
            }
        
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                        {
                            'message' : 'INVALID_PASSWORD'
                        }
                    )
    
    def test_signup_view_post_duplicated_email(self):
        client = Client()
        
        user = {
            'name'         : 'Hello Kim',
            'email'        : 'apple123@gmail.com',
            'password'     : 'Abcd1234!',
            'phone_number' : '01022224444',
            'social_id'    : '1234321'
            }
        
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                        {
                            'message' : 'DUPLICATED_EMAIL'
                        }
                    )

    def test_signup_view_post_duplicated_phone_number(self):
        client = Client()
        
        user = {
            'name'         : 'Kevin Kim',
            'email'        : 'lemon@gmail.com',
            'password'     : 'Abcd1234!',
            'phone_number' : '01011112222',
            'social_id'    : '11111'
            }
        
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                        {
                            'message' : 'DUPLICATE_PHONE_NUMBER'
                        }
                    )
    
    def test_signup_view_post_key_error(self):
        client = Client()
        user = {
            'nam'          : 'Kevin Kim',
            'email'        : 'lemon@gmail.com',
            'password'     : 'Abcd1234!',
            'phone_number' : '01022225555',
            'social_id'    : '3333'
            }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                        {
                            'message' : 'KEY_ERROR'
                        }
                    )


class UserLoginTest(TestCase):
    def setUp(self):
        hashed_password     = bcrypt.hashpw("Abcd1111!".encode('utf-8'), bcrypt.gensalt())
        db_password         = hashed_password.decode('utf-8')
        
        user = User.objects.create(
                id           = 1,
                name         = 'Owen Koh', 
                email        = 'apple123@gmail.com', 
                password     = db_password, 
                phone_number = '01011112222', 
                social_id    = '12345'
        )
        
    def tearDown(self):
        User.objects.all().delete()
        
    def test_login_view_post_user_login_success(self):
        client = Client()
        
        login_user = {
            'email'    : 'apple123@gmail.com',
            'password' : 'Abcd1111!'
        }
        
        user = User.objects.get(email = login_user['email'])
        
        if User.objects.filter(email = login_user['email']).exists():
            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = ALGORITHM)
            response     = client.post('/users/login', json.dumps(login_user), content_type = 'application/json')
            
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                        {
                            'message' : 'SUCCESS',
                            'ACCESS_TOKEN' : access_token,
                            'username' : user.name,
                            'user_id' : user.id
                        } 
                    )
    
    def test_login_view_post_user_invalid_email(self):
        client = Client()
        
        login_user = {
            'email'    : 'aple123@gmail.com',
            'password' : 'Abcd1111!'
        }
        
        if User.objects.filter(email = login_user['email']).exists():
            user         = User.objects.get(email = login_user['email'])
            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = ALGORITHM)
            
        response = client.post('/users/login', json.dumps(login_user), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                        {
                            'message' : 'INVALID_USER'
                        }
                    )
        
    def test_login_view_post_user_invalid_password(self):
        client = Client()
        
        login_user = {
            'email'    : 'apple123@gmail.com',
            'password' : 'Abcd111'
        }
        
        if User.objects.filter(email = login_user['email']).exists():
            user         = User.objects.get(email = login_user['email'])
            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = ALGORITHM)
            
        response = client.post('/users/login', json.dumps(login_user), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                        {
                            'message' : 'INVALID_PASSWORD'
                        }
                    )
        
    def test_login_view_post_user_key_error(self):
        client = Client()
        user   = {
            'emaill'   : 'apple123@gmail.com',
            'password' : 'Abcd1111!'
        }
        response = client.post('/users/login', json.dumps(user), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                        {
                            'message' : 'KEY_ERROR'
                        }
                    )

class KakaoLoginTest(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        User.objects.all().delete()
    
    @patch('users.views.requests')
    def test_kakao_login_post_new_user_success(self, mocked_requests):
        
        class KakaoResponse:
            def json(self):
                return {
                    "id": 12345,
                    "kakao_account": {
                        "profile"  : {
                            "nickname": "고영수 (Owen)"
                        },
                        "email"  : "kohys92@gmail.com"
                    }
                }
        
        mocked_requests.get = MagicMock(return_value = KakaoResponse())
        
        client    = Client()
        header    = {'HTTP_Authorization' : 'access_token'}
        response  = client.post('/users/kakaologin', content_type='application/json', **header)
        token     = response.json()['access_token']
        user_id   = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)['id']
        social_id = User.objects.get(id = user_id).social_id
        
        self.assertEqual(social_id, '12345')
        self.assertEqual(response.json(),
                         {
                             'message'      : 'SUCCESS',
                             'access_token' : token
                         })
        self.assertEqual(response.status_code, 200)
    
    @patch('users.views.requests')
    def test_kakao_login_post_user_not_exist_or_fail(self, mocked_request):
        class MockedResponse:
            def json(self):
                return {
                        "code": -401
                        }

        mocked_request.get = MagicMock(return_value=MockedResponse())
        
        client   = Client()
        header  = {'HTTP_Authorization': 'fake_token'}
        response = client.post('/users/kakaologin', content_type='application/json', **header)
        
        self.assertEqual(response.status_code, 401)
        
    def test_kakao_login_post_key_error(self):
        client   = Client()
        header   = {'Key_Error' : 'access_token'}
        response = client.post('/users/kakaologin', content_type='application/json', **header)
        
        self.assertEqual(response.status_code, 400)
        
    @patch('users.views.requests')
    def test_kakao_login_post_key_error_or_wrong_response_from_kakao(self, mocked_requests):
        
        class KakaoResponse:
            def json(self):
                return {
                    
                }
        
        mocked_requests.get = MagicMock(return_value = KakaoResponse())
        
        client    = Client()
        header    = {'HTTP_Authorization' : 'access_token'}
        response  = client.post('/users/kakaologin', content_type='application/json', **header)
        
        self.assertEqual(response.json(), {
            'message' : 'KEY_ERROR',
        })
        self.assertEqual(response.status_code, 400)