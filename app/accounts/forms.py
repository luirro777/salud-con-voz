from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField  # Importa CaptchaField


class CustomUserCreationForm(UserCreationForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Soy...",
        widget=forms.RadioSelect
    )
    captcha = CaptchaField(label="Por favor, confirma que eres humano. Escribe el sig. código ")  # Campo captcha

    class Meta:
        model = get_user_model()
        fields = ('grupo',) + UserCreationForm.Meta.fields + ('captcha',)  # Asegúrate de que captcha esté al final

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalización de los atributos de los widgets
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control h5'})
        
        # Personaliza el label de los radios para grupo
        self.fields['grupo'].label_from_instance = self.get_grupo_label 

        # Reordena manualmente los campos para que captcha esté al final
        captcha_field = self.fields.pop('captcha')
        self.fields['captcha'] = captcha_field

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        group = self.cleaned_data['grupo']
        user.groups.add(group)
        return user

    def get_grupo_label(self, obj):
        return {
            "profesional": "...profesional de la salud que realiza atención a chicos/as con parálisis cerebral y quiero colaborar.",
            "familiar": "...familiar o cuidador/a y quiero responder el cuestionario sobre calidad de vida en chicos y chicas con parálisis cerebral."
        }[obj.name]
