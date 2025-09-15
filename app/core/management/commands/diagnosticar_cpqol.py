# management/commands/diagnosticar_cpqol.py
from django.core.management.base import BaseCommand
from core.models import Cpqol

class Command(BaseCommand):
    help = 'Diagnostica problemas con cuestionarios CPQOL'

    def add_arguments(self, parser):
        parser.add_argument('codigo', type=str, help='Código del cuestionario a diagnosticar')

    def handle(self, *args, **options):
        codigo = options['codigo']
        
        try:
            cpqol = Cpqol.objects.get(codigo=codigo)
            self.stdout.write(f"Cuestionario: {cpqol.codigo}")
            self.stdout.write(f"Usuario: {cpqol.user}")
            self.stdout.write(f"Completado: {cpqol.completado}")
            self.stdout.write(f"Sección actual: {cpqol.current_seccion}")
            
            estado = cpqol.estado_secciones()
            self.stdout.write("Estado de las secciones:")
            for seccion, completada in estado.items():
                self.stdout.write(f"  {seccion}: {'Completada' if completada else 'Pendiente'}")
                
        except Cpqol.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"No se encontró un cuestionario con código {codigo}"))