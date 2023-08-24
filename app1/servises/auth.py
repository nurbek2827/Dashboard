import datetime
import random

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app1.models import User
from app1.models.auth import OTP
from methodism import code_decoder, exception_data

from app1.servises.sendotp import send_otp


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
        code = random.randint(100000, 999999)
        send_otp(data['email'], code)
        key = code_decoder(code, l=2)
        otp = OTP.objects.create(
            key=key,
            email=user.email,
            step="login",
            by=2
        )

        # cookie
        requests.session['code'] = code
        requests.session['email'] = otp.email
        requests.session['otp_token'] = otp.key
        requests.session['user_id'] = user.id

        return redirect("otp")
    return render(requests, "auth/login.html")


def sign_up(requests):
    if requests.POST:
        data = requests.POST
        user = User.objects.filter(email=data['email']).first()
        if user:
            return render(requests, "auth/regis.html", {"error": "Bu email band"})
        if data['pass'] != data['pass_conf']:
            return render(requests, "auth/regis.html", {"error": "Parollar bir biriga mos emas"})
        code = random.randint(100000, 999999)
        send_otp(data['email'], code)
        key = code_decoder(code, l=2)
        otp = OTP.objects.create(
            key=key,
            email=data["email"],
            step="regis",
            by=1,
            extra={
                "email": data['email'],
                "password": data['pass'],
                "name": data['name'],
                "last_name": data['last_name']
            }
        )

        # cookie
        requests.session['code'] = code
        requests.session['email'] = otp.email
        requests.session['otp_token'] = otp.key

        return redirect("otp")
    return render(requests, "auth/regis.html")


@login_required()
def sign_out(requests):
    logout(requests)
    return redirect("login")


def otp(requests):
    if not requests.session.get("otp_token"):
        return redirect('login')
    otp = OTP.objects.filter(key=requests.session['otp_token']).first()
    code = ''.join(x for x in requests.POST.getlist('otp'))
    print(code)
    if requests.POST:

        if not code.isdigit():
            return render(requests, "auth/otp.html", {"error": "Harf mumkin emas!"})

        if otp.is_expire:
            otp.step = 'failed'
            otp.save()
            return render(requests, "auth/otp.html", {"error": "Token eskirgan!"})

        if (datetime.datetime.now() - otp.created).total_seconds() >= 120:
            otp.is_expire = True
            otp.save()
            return render(requests, "auth/otp.html", {"error": "Vaqt tugagan"})

        if int(code_decoder(otp.key, decode=True, l=2)) != int(code):
            otp.tries += 1
            otp.save()
            return render(requests, "auth/otp.html", {"error": "Kod xato!"})


        if otp.by == 1:
            user = User.objects.create_user(**otp.extra)
            authenticate(requests)
            otp.step = 'register'
        else:
            user = User.objects.get(id=requests.session['user_id'])
            otp.step = 'logged'

        login(requests, user)
        otp.save()

        try:
            if "user_id" in requests.session:
                del requests.session['user_id']
            del requests.session['otp_token']
            del requests.session['code']
            del requests.session['email']
        except Exception as e:
            print(exception_data(e))


        return redirect('home')

    return render(requests, "auth/otp.html")



def resend_otp(requests):
    if not requests.session.get("otp_token"):
        return redirect('login')

    old = OTP.objects.filter(key=requests.session['otp_token']).first()
    old.is_expired = True
    old.step = 'failed'
    old.save()
    code = random.randint(100000, 999999)
    send_otp(old.email, code)
    key = code_decoder(code, l=2)
    otp = OTP.objects.create(
        key=key,
        email=old.email,
        step="regis" if old.by == 2 else "regis",
        by=old.by,
        extra=old.extra
    )

    # cookie
    requests.session['code'] = code
    requests.session['email'] = otp.email
    requests.session['otp_token'] = otp.key

    return redirect("otp")