import requests
import random
from django.conf import settings
from otpauth import OtpAuth

def generate_otp():
    """Cette fonction génère un code OTP aléatoire en utilisant la bibliothèque otpauth"""
    auth = OtpAuth('JBSWY3DPEHPK3PXP') # Clé secrète aléatoire
    return auth.totp()


def send_otp_to_phone(phone_number):
    try:
        otp= generate_otp(length=6)
        url = f"https://2factor.in/API/VI/{settings.API_KEY}/SMS/{phone_number}/{otp}"
        response =requests.get(url)
        return otp

    except Exception as e:
        return None