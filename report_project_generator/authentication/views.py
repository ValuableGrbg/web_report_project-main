from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.urls import reverse
from .utils import token_generator

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

# Create your views here.

# Creating a user account
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # get user data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) <= 3:
                    messages.error(request, 'Минимальный размер пароля 4 знака!')
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                # path_to_view
                # - получаем домен
                domain = get_current_site(request).domain

                # - раскодировываем id юзера
                uidb64 = urlsafe_base64_encode(force_bytes((user.pk)))

                # - создаем токен
                # token = token_generator.make_token(user)

                # - получаем относительный url для верификации
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

                activate_url = f'http://{domain}{link}'
                email_subject = 'Подтверждение регистрации. "Сибэнергодиагностика. Лаборатория"'
                email_body = f'Добрый день, {username}!\n' \
                             f'Перейдите по ссылке, чтобы подтвердить регистрацию на ресурсе' \
                             f' "Сибэнергодиагностика. Лаборатория"\n{activate_url}'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@sibenedia.ru',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Учетная запись создана!')
                # user.save()
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
            try:
                id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=id)

                if not token_generator.check_token(user, token):
                    messages.error(request, 'Аккаунт уже активирован!')
                    return redirect(f'login?message=User already activated')
                if user.is_active:
                    return redirect('login')
                user.is_active = True
                user.save()

                messages.success(request, 'Учетная запись активирована!')
                print('yo')
                return redirect('login')

            except Exception as ex:
                pass
            return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Добро пожаловать, {user.username}!')
                    return redirect('analysis_app')
                messages.error(request, 'Аккаунт не активирован, пожалуйста, проверьте почту.')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Неверные логин или пароль.')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Пожалуйста, заполните все поля.')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Вы вышли из учетной записи')
        return redirect('login')



# validate

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse(
                {'username_error': 'Имя пользователя может содержать только буквы из алфавита и цифры 0-9'},
                status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {'username_error': 'Имя пользователя занято'},
                status=409)
        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {'email_error': 'Электронная почта уже используется'},
                status=409)
        if not validate_email(email):
            return JsonResponse(
                {'email_error': 'Введите электронную почту'},
                status=400)
        # if User.objects.filter(email=email).exists():
        #     return JsonResponse(
        #         {'email_error': 'Электронная почта уже используется'},
        #         status=409)
        return JsonResponse({'email_valid': True})

