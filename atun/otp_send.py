from django.core.mail import send_mail
import random

def send_otp_via_email(email):
    otp=str(random.randint(100000, 999999))
    subject = 'Your OTP Code for Verification - Study Buddy'
    message = f'Your OTP code for verification is: {otp}. Please do not share this code with anyone.'
    from_email='indranilde92@gmail.com'
    send_mail(subject, message, from_email, [email])
    return otp