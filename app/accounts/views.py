# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django import forms
from django.views.generic import CreateView


class UserCreationCustomForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class SignUpView(CreateView):
    form_class = UserCreationCustomForm
    success_url = reverse_lazy("login")
    template_name = "registration/registro.html"