from django import forms

from .models import *


class CodigoForm(forms.Form):
    dni = forms.CharField(label="Ingrese las 3 últimos numeros del dni del paciente", max_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(label="Ingrese el primer nombre del paciente", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def save(self, user):
        dni = self.cleaned_data.get('dni')
        nombre = self.cleaned_data.get('nombre')
        codigo = f'{user.username}-{dni}-{nombre}'
        cpqol_instance = Cpqol.objects.create(
            user=user,
            codigo=codigo
        )
        return cpqol_instance



class BaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


    def save(self, cpqol, atributo):
        instance = super().save(commit=True)
        setattr(cpqol, atributo, instance)
        cpqol.save()
        return instance


class TutorForm(BaseForm):
    class Meta:
        model = Tutor
        fields = '__all__'


class PacienteForm(BaseForm):
    class Meta:
        model = Paciente
        fields = '__all__'


class SentimientosForm(BaseForm):
    class Meta:
        model = Sentimientos
        fields = '__all__'


class RelacionesForm(BaseForm):
    class Meta:
        model = Relaciones
        fields = '__all__'

class FamiliaForm(BaseForm):
    class Meta:
        model = Familia
        fields = '__all__'

class ParticipacionForm(BaseForm):
    class Meta:
        model = Participacion
        fields = '__all__'

class EscuelaForm(BaseForm):
    class Meta:
        model = Escuela
        fields = '__all__'

class SaludForm(BaseForm):
    class Meta:
        model = Salud
        fields = '__all__'

class DolorForm(BaseForm):
    class Meta:
        model = Dolor
        fields = '__all__'

class ServiciosForm(BaseForm):
    class Meta:
        model = Servicios
        fields = '__all__'










