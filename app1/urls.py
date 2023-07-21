from django.urls import path

from .servises.auth import sign_in, sign_up, sign_out
from .servises.ishchi import get_ishchi
from .views import index

urlpatterns = [
    path("", index, name="home"),
    path("ishchi/", get_ishchi, name="get_ishchi"),

    path("login", sign_in, name='login'),
    path("regis", sign_up, name='regis'),
    path("logout", sign_out, name='logout'),
]