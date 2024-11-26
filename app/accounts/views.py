# accounts/views.py

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import *

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("user_creation_success")
    template_name = "registration/registro.html"

class UsuarioCreadoView(TemplateView):
    template_name = "registration/registro_exitoso.html"