import jwt

from django.core import exceptions
from django.http import JsonResponse

from my_settings import SECRET_KEY
from users.models import User

def user_auth(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            if not access_token:
                return JsonResponse({'message' : 'NO TOKEN'}, status = 403)
            
            payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
            user_id = payload['id']
            
            user = User.objects.get(id = user_id)
            request.user = user.id
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 403)            
             
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 403)
        
        return func(self, request, *args, **kwargs)
    
    return wrapper