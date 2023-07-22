# from .models import OTP
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
import smtplib
from django.core.cache import cache
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .helpers import send_otp_to_phone
from .models import User
from rest_framework.decorators import api_view
import jwt, datetime
from django.core.cache import cache

cache.set('my_key', 'my_value' ,timeout= None)
my_value = cache.get('my_key')



# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login("")
        return Response(serializer.data)
    
@api_view(['POST'])
def send_otp(request):
        data = request.data

        if data.get('phone_number') is None :
            return Response ({
                'status' :400,
                'message' : 'key phone_number is required'
            })
        
        if data.get('password') is None:
            return Response ({
                'status' :400,
                'message' : 'key password is required'
            })
        otp = send_otp_to_phone(data.get('phone_number'))
        if otp is None:
            return Response({
                'status':500,
                'message': 'OTP fail to generate'
            })
        user = User.objects.create(
            phone_number = data.get('phone_number'),
            otp = otp,
            is_active =False
        )
        user.set_password(data.get('password'))
        user.save()
        return Response ({
                'status' :200,
                'message' : 'otp sent',
                'otp': otp
            })



@api_view(['post'])
def verify_otp(request):
        data = request.data

        if data.get('otp') is None:
            return Response ({
                'status' :400,
                'message' : 'key otp is required'
                
            })
        
        try:
            user_obj = User.objects.get(otp = data.get('otp'))
            user_obj.is_active=True

        except Exception as e:
            return Response ({
                    'status' :400,
                    'message' : 'invalid otp'
                })
        
        if user_obj.otp == data.get('otp'):
            user_obj.is_phone_verified =True
            user_obj.save()
            return Response ({
                    'status' :200,
                    'message' : 'otp matched'
                })
        
        return Response ({
                    'status' :400,
                    'message' : 'invalid otp'
                })     

class LoginView(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        password = request.data['password']

        user = User.objects.filter(phone_number=phone_number).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
                
        # Storing the token in Redis
        cache.set('jwt', token, timeout=None)

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response