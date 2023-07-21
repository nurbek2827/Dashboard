from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app1.models import Ishchi

@login_required(login_url="login")
def get_ishchi(requests):
    ctx = {
        "root": Ishchi.objects.all()
    }
    return render(requests, "ishchi/list.html", ctx)
