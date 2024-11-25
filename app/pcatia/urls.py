from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    # Vistas relacionadas al registro de la solicitud
    HomeView,
    SolicitudCreateView,
    SolicitudReviewView,
    SolicitudUpdateView,
    SolicitudConfirmView,

    # Vistas relacionadas al perfil de admin    
    SolicitudListView, 
    SolicitudDeleteView, 
    SolicitudDetailView, 
    GenerarDocumentoView, 
    DescargarDocumentoView
)

app_name = 'pcatia'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('solicitud/', SolicitudCreateView.as_view(), name='crear_solicitud'),
    path('review/', SolicitudReviewView.as_view(), name='solicitud_review'),
    path('edit/', SolicitudUpdateView.as_view(), name='solicitud_edit'),
    path('confirmar/', SolicitudConfirmView.as_view(), name='solicitud_confirmar'),    
    path('solicitudes/', SolicitudListView.as_view(), name='solicitud_list'),
    path('<int:pk>/', SolicitudDetailView.as_view(), name='solicitud_detail'),    
    path('<int:pk>/borrar/', SolicitudDeleteView.as_view(), name='solicitud_delete'),
    path('generar_documento/<int:pk>/', GenerarDocumentoView.as_view(), name='generar_documento'),
    path('descargar_documento/<str:file_name>/', DescargarDocumentoView.as_view(), name='descargar_documento'),    
]
