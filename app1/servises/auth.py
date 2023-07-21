from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app1.models import User


def sign_in(requests):
    if not requests.user.is_anonymous:
        return redirect('home')

    if requests.POST:
        data = requests.POST
        user = User.objects.filter(email=data['email']).first()
        if not user:
            return render(requests, "auth/login.html", {"error": "Password yoki email xato"})
        if not user.check_password(data['pass']):
            return render(requests, "auth/login.html", {"error": "Password yoki email xato"})
        if not user.is_active:
            return render(requests, "auth/login.html", {"error": "User aktiv holatda emas"})

        login(requests, user)
        return redirect("home")
    return render(requests, "auth/login.html")


def sign_up(requests):
    if requests.POST:
        data = requests.POST
        user = User.objects.filter(email=data['email']).first()
        if user:
            return render(requests, "auth/regis.html", {"error": "Bu email band"})
        if data['pass'] != data['pass_conf']:
            return render(requests, "auth/regis.html", {"error": "Parollar bir biriga mos emas"})
        user = User.objects.create_user(email=data['email'],
                                        password=data['pass'],
                                        name=data['name'],
                                        last_name=data['last_name']
                                        )
        authenticate(requests)
        login(requests, user)
        return redirect('home')
    return render(requests, "auth/regis.html")


@login_required()
def sign_out(requests):
    logout(requests)
    return redirect("login")
