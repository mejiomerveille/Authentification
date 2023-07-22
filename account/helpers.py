from .models import User
import random
from django.conf import settings
from django.core.mail import send_mail


def send_otp_to_phone(phone_number):
        if phone_number is not None:
            otp = random.randint(1000, 9999)
            # url = f"https://2factor.in/API/VI/{settings.API_KEY}/SMS/{phone_number}/{otp}"
            # response = requests.get(url)
            return str(otp)
        return None


def send_otp_email(otp, recipient, email):
        if email is not None:
            otp = random.randint(1000, 9999)
            subject = 'Votre OTP'
            message = f'Votre OTP est {otp}. Ne le partagez avec personne.'
            sender = 'email'
            recipient_list = [recipient]

            send_mail(subject, message, sender, recipient_list)
            return str(otp)
        return None