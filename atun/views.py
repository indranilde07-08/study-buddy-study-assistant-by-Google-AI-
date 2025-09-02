from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from .otp_send import send_otp_via_email
from django.core.mail import send_mail
import sys

def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        if 'create' in request.POST:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already exists')
                return redirect('atun:signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
                return redirect('atun:signup')
            try:
                User.objects.create_user(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password']
                )
                messages.success(request,'Account created successfully')

                subject = 'Welcome to Study Buddy'
                message = f'Hi {request.POST["first_name"]}, thank you for registering at Study Buddy. We are excited to have you on board!\n'\
                'If you have any questions or need assistance, feel free to reach out to our support team.\n'\
                'Happy studying!\n'\
                'Best regards,\n'\
                'The Study Buddy Team'


                from_email='indranilde92@gmail.com'
                send_mail(subject, message, from_email, [request.POST['email']])
                return redirect('atun:signin')
            except InterruptedError:
                messages.error(request,'Error creating account')
                return redirect('atun:signup')
        elif 'reset' in request.POST:
            return redirect('atun:signup')
    return render(request, 'signup.html')
def signin(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            user=authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password']
            )
            if user:
                login(request,user)
                messages.success(request,'Successfully Logged In')
                subject = 'Login Notification - Study Buddy'
                message = f'Hi {user.first_name}, you have successfully logged into your Study Buddy account\n.\
                If you have any questions or need assistance, please don\'t hesitate to contact our support team.that email id: indranilde92@gmail.com\n\
                "thank you for using our services!"'
                from_email='indranilde92@gmail.com'
                send_mail(subject, message, from_email, [user.email])
                return redirect('home:view')
            else:
                messages.error(request,'Invalid Credentials')
                return redirect('atun:signin')
        elif 'reset' in request.POST:
            return redirect('atun:signin')
    return render(request, 'signin.html')

def email_send(request):
    if request.method == 'POST':
        user_name=request.POST['username']
        user_email=request.POST['email']
        if User.objects.filter(username=user_name,email=user_email).exists():
            otp=send_otp_via_email(user_email)
            request.session['otp']=otp
            request.session['user_name']=user_name
            messages.success(request,'OTP sent to your email')
            return redirect('atun:verify')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('atun:email_send')
    return render(request, 'email_send.html')

def verify_otp(request):
    original_otp=request.session.get('otp')
    if request.method == 'POST':
        user_otp = request.POST['otp']
        if original_otp == user_otp:
            messages.success(request,'OTP verified successfully')
            return redirect('atun:change_password')
        else:
            messages.error(request,'Invalid OTP')
            return redirect('atun:verify')
    return render(request, 'verify_otp.html')

def change_password(request):
    if request.method == 'POST':
        user_name=request.session.get('user_name')
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        if 'change' in request.POST:
            if new_password != confirm_password:
                messages.error(request,'Passwords do not match')
                return redirect('atun:change_password')
            else:
                try:
                    user=User.objects.get(username=user_name)
                    if user.check_password(new_password):
                        messages.error(request,'New password cannot be the same as the old password')
                        return redirect('atun:change_password')
                    else:
                        user.set_password(new_password)
                        user.save()
                        messages.success(request,'Password changed successfully')
                        subject = 'Password Change Notification - Study Buddy'
                        message = f'Hi {user.first_name}, your password has been changed successfully.\n'\
                        'If you did not initiate this change, please contact our support team immediately.\n'\
                        'Best regards,\n'\
                        'The Study Buddy Team'

                        from_email='indranilde92@gmail.com'
                        send_mail(subject, message, from_email, [user.email])
                        return redirect('atun:signin')
                except User.DoesNotExist:
                    messages.error(request,'User does not exist')
                    return redirect('atun:change_password')
    return render(request, 'change_password.html')

def logout_user(request):
    logout(request)
    return redirect('atun:signin')

def profile(request):
    return render(request, 'profile.html',{'user':request.user})

def update(request):
    if request.method == 'POST':
        user=request.user
        sys.stdout.write(str(user))
        sys.stdout.flush()
        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.email=request.POST['email']
        user.username=request.POST['user_name']
        user.save()
        messages.success(request,'Profile updated successfully')
        subject='Profile Update Notification - Study Buddy'
        message=f'Hi {user.first_name}, your profile has been updated successfully.\n'\
        'If you did not initiate this update, please contact our support team immediately.\n'\
        'Best regards,\n'\
        'The Study Buddy Team'

        from_email='indranilde92@gmail.com'
        send_mail(subject, message, from_email, [user.email])
    
        return redirect('atun:profile')
    return render(request, 'update_profile.html')

def update_password(request):
    user = request.user
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if not user.check_password(old_password):
            messages.error(request,'Old password is incorrect')
        elif new_password != confirm_password:
            messages.error(request,'Passwords do not match')
        elif user.check_password(new_password):
            messages.error(request,'New password cannot be the same as the old password')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Password changed successfully')
            subject='Password Change Notification - Study Buddy'
            message=f'Hi {user.first_name}, your password has been changed successfully.\n'\
            'If you did not initiate this change, please contact our support team immediately.\n'\
            'Best regards,\n'\
            'The Study Buddy Team'
            from_email='indranilde92@gmail.com'
            send_mail(subject, message, from_email, [user.email])
            return redirect('atun:profile')
    return render(request, 'update_password.html')

def tutorial(request):
    return render(request, 'tutorial.html')



