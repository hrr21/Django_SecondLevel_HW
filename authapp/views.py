from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from basketapp.models import Basket
from django.core.mail import send_mail
from django.conf import settings
from authapp.models import User


def send_verify_mail(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])

    subject = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and user.is_activation_key_expired():
            user.is_active = True

            user.save()
            auth.login(request, user)
        return render(request, 'authapp/verification.html')
    except Exception as ex:
        return HttpResponseRedirect(reverse('main'))


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'authapp/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('authapp:login'))
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'authapp/register.html', context)


def profile(request):
    title = 'редактирование'

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authapp:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)
    baskets = Basket.objects.filter(user=request.user)
    context = {
        'title': title,
        'form': form,
        'baskets': baskets,
        'profile_form': profile_form
    }

    return render(request, 'authapp/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))
