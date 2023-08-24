from django.urls import path

from .servises.auth import sign_in, sign_up, sign_out, otp, resend_otp
from .servises.ishchi import get_ishchi_delete, add, edit
from .views import index

urlpatterns = [
    path("", index, name="home"),

    # crud
    path("ishchi/", get_ishchi_delete, name="get_ishchi"),
    path("det/<int:pk>/", get_ishchi_delete, name="get_det"),
    path("del/<int:delete_id>/", get_ishchi_delete, name="delete"),
    path("add/", add, name="add"),
    path("edit/<int:pk>/", edit, name="edit"),

 #auth
    path("login/", sign_in, name='login'),
    path("regis/", sign_up, name='regis'),
    path("logout/", sign_out, name='logout'),
    path("otp/", otp, name='otp'),
    path("resend/otp/", resend_otp, name='re-otp'),
]