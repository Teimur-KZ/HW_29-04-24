from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .user_form import SignUpForm, ProfileForm, LoginForm
from .models import Profile
from django.shortcuts import get_object_or_404


def profile_view(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        return render(request, 'profile.html', {'profile': profile})
    else:
        return redirect('login') # если пользователь не авторизован, перенаправляем на страницу авторизации



def signup_view(request):
    '''Представление для регистрации нового пользователя'''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'signup.html', {'form': form, 'profile_form': profile_form})

from django.contrib.auth import get_user_model

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Очистите все старые сообщения
            messages.set_level(request, messages.ERROR)
            storage = messages.get_messages(request)
            storage.used = True

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            '''Нужно получить пользователя по email и аутентифицировать его по паролю'''
            User = get_user_model() # получаем модель пользователя
            try: # пытаемся получить пользователя по email
                user = User.objects.get(email=email)
                print('найден email:', email)
            except User.DoesNotExist: # если пользователя нет, то user = None
                user = None
                print('не найден email:', email)
            if user is not None: # если пользователь существует
                user = authenticate(username=user.username, password=password)
                if user is not None: # если пользователь аутентифицирован
                    print('аутентификация прошла успешно')
                    login(request, user)
                    return redirect('home')
                else: # если пароль не верный
                    messages.error(request, 'Неверный пароль')
            else: # если пользователя нет
                print('Пользователь с таким email не найден')
                messages.error(request, 'Пользователь с таким email не найден')
    else: # если метод GET
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'title': 'Авторизация'})







def logout_view(request):
    '''Представление для выхода пользователя'''
    logout(request)
    return redirect('home') # не забыть создать представление home и маршрут к нему


