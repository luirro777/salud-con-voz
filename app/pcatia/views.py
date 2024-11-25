# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# Vistas
from django.views.generic import (DetailView, DeleteView, ListView, TemplateView, View, UpdateView, CreateView)
from django.views.generic.edit import FormView

# Models
from .models import Solicitud
from .forms import SolicitudForm

# Apps de terceros
from docxtpl import DocxTemplate
import uuid
import os


class HomeView(TemplateView):
    template_name = "pcatia/home.html"


class SolicitudCreateView(FormView):    
    form_class = SolicitudForm
    template_name = 'pcatia/solicitud_form.html'
    success_url = reverse_lazy('pcatia:solicitud_review')

    def form_valid(self, form):
        # Concatenar los campos del teléfono
        codigo_internacional = form.cleaned_data.get('codigo_internacional')
        codigo_area = form.cleaned_data.get('codigo_area')
        numero_telefono = form.cleaned_data.get('numero_telefono')

        codigo_internacional_alterno = form.cleaned_data.get('codigo_internacional_alterno')
        codigo_area_alterno = form.cleaned_data.get('codigo_area_alterno')
        numero_telefono_alterno = form.cleaned_data.get('numero_telefono_alterno')

        telefono_principal = f"{codigo_internacional} ({codigo_area}) {numero_telefono}"
        telefono_alterno = f"{codigo_internacional_alterno} ({codigo_area_alterno}) {numero_telefono_alterno}"

        # Asignar los valores concatenados a los campos del modelo
        solicitud = form.save(commit=False)
        solicitud.telefono_principal = telefono_principal
        solicitud.telefono_alterno = telefono_alterno

        self.request.session['form_data'] = form.cleaned_data
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Formulario es inválido")
        print(form.errors)  # Imprime los errores en la consola
        return super().form_invalid(form)


class SolicitudReviewView(TemplateView):    
    template_name = 'pcatia/solicitud_review.html'    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_data'] = self.request.session.get('form_data', {})
        return context
    
class SolicitudUpdateView(FormView):    
    form_class = SolicitudForm
    template_name = 'pcatia/solicitud_form.html'
    
    def get_form(self, form_class=None):
        # Prepopulate the form with data from the session
        form = super().get_form(form_class)
        form.initial = self.request.session.get('form_data', {})
        return form

    def form_valid(self, form):
        self.request.session['form_data'] = form.cleaned_data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pcatia:solicitud_review')
'''
class SolicitudConfirmView(TemplateView):    
    template_name = 'pcatia/solicitud_confirmar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_data'] = self.request.session.get('form_data', {})
        return context

    def post(self, request, *args, **kwargs):
        form_data = request.session.get('form_data', {})
        if form_data:
            # Save the form data to the database
            form_data.pop('captcha', None)  # Elimina 'captcha' si existe
            Solicitud.objects.create(**form_data)
            # Clear the session data
            request.session.pop('form_data', None)
        return self.render_to_response(self.get_context_data())
'''
class SolicitudConfirmView(TemplateView):    
    template_name = 'pcatia/solicitud_confirmar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_data'] = self.request.session.get('form_data', {})
        return context

    def post(self, request, *args, **kwargs):
        form_data = request.session.get('form_data', {})
        if form_data:            
            # Armar los campos de telefono
            telefono_principal = f"{form_data.get('codigo_internacional', '')} {form_data.get('codigo_area', '')} {form_data.get('numero_telefono', '')}"
            telefono_alterno = f"{form_data.get('codigo_internacional_alterno', '')} {form_data.get('codigo_area_alterno', '')} {form_data.get('numero_telefono_alterno', '')}"
            
            # Eliminar los campos desglosados del form_data
            form_data.pop('codigo_internacional', None)
            form_data.pop('codigo_area', None)
            form_data.pop('numero_telefono', None)
            form_data.pop('codigo_internacional_alterno', None)
            form_data.pop('codigo_area_alterno', None)
            form_data.pop('numero_telefono_alterno', None)

            # Agregar los teléfonos completos al form_data
            form_data['telefono_principal'] = telefono_principal
            form_data['telefono_alterno'] = telefono_alterno

            form_data.pop('captcha', None)  # Elimina 'captcha' si existe
            solicitud = Solicitud.objects.create(**form_data)

            # Enviar correo electrónico con los datos del formulario
            subject = 'Nueva solicitud recibida'
            # Renderizamos un template HTML para el contenido del email
            html_message = render_to_string('pcatia/email_template.html', {'solicitud': solicitud})
            plain_message = strip_tags(html_message)
            from_email = f'{settings.EMAIL_HOST_NAME} <{settings.EMAIL_HOST_USER}>'
            to = settings.EMAIL_RECEIVER

            send_mail(
                subject,
                plain_message,
                from_email,
                [to],
                html_message=html_message,  # Envía el mensaje HTML si el cliente lo soporta
                fail_silently=False,
            )

            # Clear the session data
            request.session.pop('form_data', None)
        
        return self.render_to_response(self.get_context_data())


class SolicitudListView(LoginRequiredMixin, ListView):
    model = Solicitud
    template_name = 'pcatia/solicitud_list.html'
    context_object_name = 'pcatia'    

class SolicitudDeleteView(LoginRequiredMixin, DeleteView):
    model = Solicitud
    template_name = 'pcatia/solicitud_confirm_delete.html'
    success_url = reverse_lazy('pcatia:solicitud_list')

class SolicitudDetailView(LoginRequiredMixin, DetailView):
    model = Solicitud
    template_name = 'pcatia/solicitud_detail.html'

# Generacion de docx
class GenerarDocumentoView(LoginRequiredMixin, DetailView):
    model = Solicitud
    template_name = 'pcatia/generar_documento.html'  

    def get(self, request, *args, **kwargs):
        solicitud = self.get_object()

        # Cargar la plantilla del archivo .docx
        template = DocxTemplate('templates/ActaUso.docx')

        # Definir el contexto con los datos del formulario
        contexto = {            
            'nombres_principal': solicitud.nombres_principal,
            'apellidos_principal': solicitud.apellidos_principal,
            'cargo_principal': solicitud.cargo_principal,
            'institucion_principal': solicitud.institucion_principal,
            'ciudad_principal': solicitud.ciudad_principal,
            'pais_principal': solicitud.pais_principal,
            'titulo_estudio': solicitud.titulo_estudio, 
            'caracteristicas_poblacion': solicitud.caracteristicas_poblacion,
            'dia_solicitud': solicitud.fecha_solicitud.day,
            'mes_solicitud': solicitud.fecha_solicitud.month,
            'anio_solicitud': solicitud.fecha_solicitud.year,          
        }

        # Rellenar la plantilla
        template.render(contexto)

        # Generar un nombre único para el archivo
        file_name = f'documento_{uuid.uuid4()}.docx'

        # Guardar el archivo temporalmente
        file_path = os.path.join('media', 'temp_docs', file_name)
        template.save(file_path)

        # Redirigir a la vista de descarga con el archivo generado
        return redirect('pcatia:descargar_documento', file_name=file_name)

class DescargarDocumentoView(LoginRequiredMixin, View):
    
    def get(self, request, file_name):
        file_path = os.path.join('media', 'temp_docs', file_name)

        # Comprobar si el archivo existe
        if default_storage.exists(file_path):
            # Crear una respuesta HTTP con el archivo
            with default_storage.open(file_path, 'rb') as docx_file:
                response = HttpResponse(docx_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = f'attachment; filename={file_name}'
                return response
        else:
            return HttpResponse("El enlace ha expirado o el archivo ya no está disponible.", status=404)