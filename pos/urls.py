from django.urls import path

from pos.views import pos_terminal

urlpatterns = [
    path("", pos_terminal, name="pos-terminal"),
]
