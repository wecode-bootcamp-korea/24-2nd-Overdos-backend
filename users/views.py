import json
import re
import bcrypt
import jwt
import requests

from django.views import View
from django.http import JsonResponse

from .models import User
from my_settings import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not re.search('[a-zA-Z0-9.+-]+@'
                                        '[a-zA-Z0-9-]+\.'
                                        '[a-zA-Z0-9.]+', data['email']) :
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)

            if not re.fullmatch('^(?=.*[a-z])(?=.*[A-Z])'
                                        '(?=.*\d)(?=.*[@$!%*?&])'
                                        '[A-Za-z\d@$!%*?&]{8,10}$', data['password']):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
            
            if User.objects.filter(phone_number = data['phone_number']).exists():
                return JsonResponse({'message' : 'DUPLICATE_PHONE_NUMBER'}, status = 400)
            
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : 'DUPLICATED_EMAIL'}, status = 400)
            
            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(), 
                phone_number = data['phone_number'],
                social_id    = data['social_id'],
            )
            
            return JsonResponse({'message' : 'CREATED'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')) or data['password'] is None:
                    access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
                    return JsonResponse({'message' : 'SUCCESS', 'ACCESS_TOKEN' : access_token, 'username' : user.name, 'user_id' : user.id}, status = 200)
                
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 401)

            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        
class KakaoLoginView(View):
    def post(self, request):
        try:
            access_token = request.headers['Authorization']
            KAKAO_URL    = "https://kapi.kakao.com/v2/user/me"
            header       = {'Authorization' : 'Bearer {}'.format(access_token)}
            
            response = requests.get(KAKAO_URL, headers = header).json()
            
            if response.get('code') == -401:
                return JsonResponse({'message':'INVALID_TOKEN'}, status=401)
            
            user, is_user = User.objects.get_or_create(
                name      = response['kakao_account']['profile']['nickname'],
                email     = response['kakao_account']['email'],
                social_id = response['id'],
                )

            token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'message' : 'SUCCESS', 'access_token' : token}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)