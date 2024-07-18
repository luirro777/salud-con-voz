from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):


    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Soy...",
        widget=forms.RadioSelect
    )

    class Meta:
        model = get_user_model()
        fields = ('grupo',) + UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control h5'})          
        self.fields['grupo'].label_from_instance = self.get_grupo_label 

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