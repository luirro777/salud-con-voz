from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .resources import CpqolResource
from .help_texts import SUBTITULOS

from .forms import *

# Create your views here.

""""
@login_required
def vista_formulario(request):
    grupo = request.user.groups.first().name if request.user.groups.all() else "profesional"
    print(f"Grupo del usuario: {grupo}")

    # Obtenemos el número de sección y código desde la URL
    numero_seccion = int(request.GET.get('seccion', 0))
    codigo_from_url = request.GET.get('codigo') 

    cpqol = None # Inicializar cpqol a None    

    # **Lógica para obtener la instancia principal de CPQOL/CPQOLProfesional**
    # Cargar cpqol si hay un código en la URL, para cualquier sección excepto la 0.
    # La sección 0 es donde se inicia un NUEVO cuestionario, sin código todavía.
    if codigo_from_url and numero_seccion > 0: 
        try:
            if grupo == "profesional":
                cpqol = CpqolProfesional.objects.get(user=request.user, codigo=codigo_from_url)
            else:
                cpqol = Cpqol.objects.get(user=request.user, codigo=codigo_from_url)
        except (Cpqol.DoesNotExist, CpqolProfesional.DoesNotExist):
            # Si el código no corresponde a un CPQOL/CPQOLProfesional existente para este usuario,
            # redirigir a la sección de código para que el usuario pueda ingresar uno o crear uno nuevo.           
            return redirect(reverse('cpqol') + '?seccion=1') # Redirige a la sección de código
   
    # Definimos las secciones del formulario
    # TyC y código es común a todos los grupos 
    secciones = [
        {'form': TerminosYCondicionesForm, 'nombre': "Términos y condiciones", 'subtitulo': SUBTITULOS['terminos_y_condiciones']},
        {'form': CodigoForm, 'nombre': "Código de participante", 'subtitulo': SUBTITULOS['codigo_participante']},
    ]
    if grupo == "profesional":
        secciones.extend([
            {'form': ProfesionalForm, 'attr': "profesional", 'nombre': "Caracterización del profesional y el lugar de atención", 'subtitulo': SUBTITULOS['profesional_caracterizacion']},
            {'form': ContextoForm, 'attr': "contexto", "nombre": "Datos generales del NNAJ y su contexto", 'subtitulo': SUBTITULOS['profesional_contexto']},
            {'form': DatosClinicosForm, 'attr': "datos_clinicos", 'nombre': "Datos clínicos del NNAJ", 'subtitulo': SUBTITULOS['profesional_datos_clinicos']},
            {'form': FinalizacionForm, 'attr': "correo", 'nombre': "Finalizar cuestionario", 'subtitulo': SUBTITULOS['profesional_finalizacion']},
        ])
    else:
        secciones.extend([
            {'form': TutorForm, 'attr': "tutor", 'nombre': "Padre, madre o cuidador", 'subtitulo': SUBTITULOS['familiar_tutor']},
            {'form': PacienteForm, 'attr': "paciente", 'nombre': "Paciente", 'subtitulo': SUBTITULOS['familiar_paciente']},
            {'form': MovimientoForm, 'attr': "movimiento", 'nombre': "Movilidad", 'subtitulo': SUBTITULOS['familiar_movilidad']},
            {'form': SentimientosForm, 'attr': "sentimientos", 'nombre': "Calidad de vida del niño/a o adolescente con parálisis cerebral", 'subtitulo': SUBTITULOS['familiar_sentimientos']},
            {'form': RelacionesForm, 'attr': "relaciones", 'nombre': "Relaciones con los demás", 'subtitulo': SUBTITULOS['familiar_relaciones']},
            {'form': FamiliaForm, 'attr': "familia", 'nombre': "Familia", 'subtitulo': SUBTITULOS['familiar_familia']},
            {'form': ParticipacionForm, 'attr': "participacion", 'nombre': "Participacion", 'subtitulo': SUBTITULOS['familiar_participacion']},
            {'form': EscuelaForm, 'attr': "escuela", 'nombre': "Escuela o Colegio", 'subtitulo': SUBTITULOS['familiar_escuela']},
            {'form': SaludForm, 'attr': "salud", 'nombre': "Salud", 'subtitulo': SUBTITULOS['familiar_salud']},
            {'form': DolorForm, 'attr': "dolor", 'nombre': "Dolor y molestias", 'subtitulo': SUBTITULOS['familiar_dolor']},
            {'form': ServiciosForm, 'attr': "servicios", 'nombre': "Acceso a servicios", 'subtitulo': SUBTITULOS['familiar_servicios']},
            {'form': SaludUltimaSemanaForm, 'attr': "salud_ultima_semana", 'nombre': "Más preguntas sobre la salud del niño/a o adolescente", 'subtitulo': SUBTITULOS['familiar_salud_ultima_semana']},
            {'form': SaludUltimaSemana2Form, 'attr': "salud_ultima_semana_2", 'nombre': "Sobre la salud del chico o chica", 'subtitulo': SUBTITULOS['familiar_salud_ultima_semana_2']},
            {'form': HogarForm, 'attr': "hogar", 'nombre': "Características del hogar", 'subtitulo': SUBTITULOS['familiar_hogar']},
            {'form': FinalizacionForm, 'attr': "correo", 'nombre': "Finalizar cuestionario", 'subtitulo': SUBTITULOS['familiar_finalizacion']},
            {'form': None, 'nombre': "Informe de resultados", 'subtitulo': SUBTITULOS['resultados']},
        ])

    total_secciones = len(secciones) - 1
    print(f"Total de secciones: {total_secciones}")

    seccion = secciones[numero_seccion]
    seccion['numero'] = numero_seccion
    seccion['siguiente'] = numero_seccion + 1
    if numero_seccion > 1:
        seccion['anterior'] = numero_seccion - 1
    seccion['grupo'] = grupo

    current_form = seccion['form']

    if request.method == 'POST': # POST request
        # Instancia el formulario con los datos POST
        if numero_seccion == 0:
            form = current_form(request.user, data=request.POST)
        elif numero_seccion == 1:
            form = current_form(request.user, grupo=grupo, data=request.POST)
        else:
            form = current_form(instance=getattr(cpqol, seccion['attr'].lower(), None), data=request.POST)

        if grupo == "familiar" and seccion['attr'] == "movimiento":
                edad = request.session.get('edad_paciente')
                form = current_form(edad=edad, data=request.POST)        
        
        # Logica una vez verificado el formulario
        if form.is_valid(): # Secciones de TyC y código
            if numero_seccion == 0:
                return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion + 1}')
            elif numero_seccion == 1:
                cpqol = form.save()
            
            # lógica de finalización
            elif (grupo == "profesional" and numero_seccion == 5) or (grupo == "familiar" and numero_seccion == 16):
    
                # 1. Guarda el formulario de finalización y la instancia principal del cuestionario
                instance = form.save(cpqol, seccion['attr'].lower())
                cpqol.completado = True
                cpqol.save()

                # 2. Maneja la redirección según el grupo
                if grupo == "profesional":
                    return redirect(reverse('home'))
                
                else:  # grupo == "familiar"
                    # Redirige a la siguiente sección, que es la de resultados (sección 16)
                    return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion + 1}&codigo={cpqol.codigo}')
            
            # Lógica para el resto de secciones intermedias
            else:
                instance = form.save(cpqol, seccion['attr'].lower())
            
            # Lógica para guardar la edad en la sesión (se ejecuta después de guardar la instancia)
            if grupo == "familiar" and seccion.get('attr') == "paciente":
                request.session['edad_paciente'] = instance.edad
            
            return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion + 1}&codigo={cpqol.codigo}')
        
        # Si el formulario no es válido, se mostrarán los errores.
        
            
    
    else: # GET request
        # Secciones de TyC y codigo
        if numero_seccion == 0:
            form = current_form(request.user)
        elif numero_seccion == 1:
            form = current_form(request.user, grupo=grupo)
        # Sección de resultados
        elif grupo == "familiar" and numero_seccion == 17:
            # Aquí va toda la lógica para obtener los resultados
            if cpqol and hasattr(cpqol, 'resultados'):
                try:
                    resultados_data = cpqol.resultados 
                    labels = list(resultados_data.keys())
                    values = list(resultados_data.values())
                except AttributeError as e:                
                    labels = []
                    values = []
            else:
                labels = []
                values = []
            # No hay formulario para renderizar en esta sección
            form = None 
        # Para todas las otras secciones
        elif numero_seccion > 1 and cpqol:
            instance = getattr(cpqol, seccion['attr'].lower(), None)
            # Para familiares
            if grupo == "familiar":
                if seccion['attr'] == "movimiento": 
                    edad = request.session.get('edad_paciente')# Guardar edad en sesión
                    try:
                        edad = int(edad)
                    except (ValueError, TypeError):
                        edad = None
                    form = current_form(edad=edad, instance=instance)
                elif numero_seccion == 17: # Resultados
                    if cpqol and hasattr(cpqol, 'resultados'):
                        try:
                            resultados_data = cpqol.resultados 
                            labels = list(resultados_data.keys())
                            values = list(resultados_data.values())
                        except AttributeError:
                            labels = []
                            values = []
                    else:
                        labels = []
                        values = []
                    # No hay formulario para renderizar en esta sección
                    form = None
                else: # Resto de las secciones
                    form = current_form(instance=instance)
            # Para profesionales
            elif grupo == "profesional":
                form = current_form(instance=instance)
        else: # Manejo de secciones 0 y 1 si no hay un cpqol
            form = current_form(request.user, grupo=grupo) if numero_seccion == 1 else current_form(request.user)
        
    return render(request, "core/formulario.html", locals())
"""
@login_required
def vista_formulario(request):
    grupo = request.user.groups.first().name if request.user.groups.all() else "profesional"
    print(f"Grupo del usuario: {grupo}")

    # Obtenemos el número de sección y código desde la URL
    numero_seccion = int(request.GET.get('seccion', 0))
    codigo_from_url = request.GET.get('codigo') 

    cpqol = None

    # Lógica para obtener la instancia principal de CPQOL/CPQOLProfesional
    if codigo_from_url and numero_seccion > 0: 
        try:
            if grupo == "profesional":
                cpqol = CpqolProfesional.objects.get(user=request.user, codigo=codigo_from_url)
            else:
                cpqol = Cpqol.objects.get(user=request.user, codigo=codigo_from_url)
        except (Cpqol.DoesNotExist, CpqolProfesional.DoesNotExist):
            return redirect(reverse('cpqol') + '?seccion=1')
   
    # Definimos las secciones del formulario
    secciones = [
        {'form': TerminosYCondicionesForm, 'nombre': "Términos y condiciones", 'subtitulo': SUBTITULOS['terminos_y_condiciones']},
        {'form': CodigoForm, 'nombre': "Código de participante", 'subtitulo': SUBTITULOS['codigo_participante']},
    ]
    
    if grupo == "profesional":
        secciones.extend([
            {'form': ProfesionalForm, 'attr': "profesional", 'nombre': "Caracterización del profesional y el lugar de atención", 'subtitulo': SUBTITULOS['profesional_caracterizacion']},
            {'form': ContextoForm, 'attr': "contexto", "nombre": "Datos generales del NNAJ y su contexto", 'subtitulo': SUBTITULOS['profesional_contexto']},
            {'form': DatosClinicosForm, 'attr': "datos_clinicos", 'nombre': "Datos clínicos del NNAJ", 'subtitulo': SUBTITULOS['profesional_datos_clinicos']},
            {'form': FinalizacionForm, 'attr': "correo", 'nombre': "Finalizar cuestionario", 'subtitulo': SUBTITULOS['profesional_finalizacion']},
        ])
    else:
        secciones.extend([
            {'form': TutorForm, 'attr': "tutor", 'nombre': "Padre, madre o cuidador", 'subtitulo': SUBTITULOS['familiar_tutor']},
            {'form': PacienteForm, 'attr': "paciente", 'nombre': "Paciente", 'subtitulo': SUBTITULOS['familiar_paciente']},
            {'form': MovimientoForm, 'attr': "movimiento", 'nombre': "Movilidad", 'subtitulo': SUBTITULOS['familiar_movilidad']},
            {'form': SentimientosForm, 'attr': "sentimientos", 'nombre': "Calidad de vida del niño/a o adolescente con parálisis cerebral", 'subtitulo': SUBTITULOS['familiar_sentimientos']},
            {'form': RelacionesForm, 'attr': "relaciones", 'nombre': "Relaciones con los demás", 'subtitulo': SUBTITULOS['familiar_relaciones']},
            {'form': FamiliaForm, 'attr': "familia", 'nombre': "Familia", 'subtitulo': SUBTITULOS['familiar_familia']},
            {'form': ParticipacionForm, 'attr': "participacion", 'nombre': "Participacion", 'subtitulo': SUBTITULOS['familiar_participacion']},
            {'form': EscuelaForm, 'attr': "escuela", 'nombre': "Escuela o Colegio", 'subtitulo': SUBTITULOS['familiar_escuela']},
            {'form': SaludForm, 'attr': "salud", 'nombre': "Salud", 'subtitulo': SUBTITULOS['familiar_salud']},
            {'form': DolorForm, 'attr': "dolor", 'nombre': "Dolor y molestias", 'subtitulo': SUBTITULOS['familiar_dolor']},
            {'form': ServiciosForm, 'attr': "servicios", 'nombre': "Acceso a servicios", 'subtitulo': SUBTITULOS['familiar_servicios']},
            {'form': SaludUltimaSemanaForm, 'attr': "salud_ultima_semana", 'nombre': "Más preguntas sobre la salud del niño/a o adolescente", 'subtitulo': SUBTITULOS['familiar_salud_ultima_semana']},
            {'form': SaludUltimaSemana2Form, 'attr': "salud_ultima_semana_2", 'nombre': "Sobre la salud del chico o chica", 'subtitulo': SUBTITULOS['familiar_salud_ultima_semana_2']},
            {'form': HogarForm, 'attr': "hogar", 'nombre': "Características del hogar", 'subtitulo': SUBTITULOS['familiar_hogar']},
            {'form': FinalizacionForm, 'attr': "correo", 'nombre': "Finalizar cuestionario", 'subtitulo': SUBTITULOS['familiar_finalizacion']},
            {'form': None, 'nombre': "Informe de resultados", 'subtitulo': SUBTITULOS['resultados']},
        ])

    total_secciones = len(secciones) - 1

    # VERIFICACIÓN 1: ¿La sección solicitada existe?
    if numero_seccion < 0 or numero_seccion >= len(secciones):
        # Si la sección no existe, redirigir a la sección apropiada
        if cpqol:
            # Si existe un cuestionario, redirigir a la sección actual del usuario
            seccion_actual = cpqol.current_seccion
            # Asegurarnos de que la sección actual esté dentro del rango válido
            if seccion_actual < 0 or seccion_actual >= len(secciones):
                seccion_actual = 0
            return redirect(reverse('cpqol') + f'?seccion={seccion_actual}' + (f'&codigo={cpqol.codigo}' if cpqol.codigo else ''))
        else:
            # Si no hay cuestionario, redirigir a la primera sección
            return redirect(reverse('cpqol') + '?seccion=0')

    # VERIFICACIÓN 2: ¿El usuario tiene permiso para acceder a esta sección?
    if cpqol:
        # Si tenemos una instancia de cuestionario, usar su propiedad current_seccion
        seccion_permitida = cpqol.current_seccion
        
        # DEBUG: Imprimir información para diagnóstico
        print(f"CPQOL: {cpqol.codigo}, Sección actual: {seccion_permitida}, Sección solicitada: {numero_seccion}")
        
        # Si el usuario intenta acceder a una sección posterior a la permitida, redirigirlo
        if numero_seccion > seccion_permitida:
            print(f"Redirigiendo a sección permitida: {seccion_permitida}")
            return redirect(reverse('cpqol') + f'?seccion={seccion_permitida}' + (f'&codigo={codigo_from_url}' if codigo_from_url else ''))
    else:
        # Si no hay cuestionario, solo puede acceder a las primeras dos secciones
        seccion_permitida = 1  # Máximo puede estar en la sección 1 (código)
        
        # Si el usuario intenta acceder a una sección posterior a la permitida, redirigirlo
        if numero_seccion > seccion_permitida:
            return redirect(reverse('cpqol') + f'?seccion={seccion_permitida}')
    
    # Si el usuario intenta acceder a una sección anterior, está permitido (puede retroceder)
    # Continuamos con el procesamiento normal...

    seccion = secciones[numero_seccion]
    seccion['numero'] = numero_seccion
    seccion['siguiente'] = numero_seccion + 1 if numero_seccion < total_secciones else None
    if numero_seccion > 0:
        seccion['anterior'] = numero_seccion - 1
    seccion['grupo'] = grupo

    current_form = seccion['form']

    # Preparar los argumentos para el formulario
    form_kwargs = {}
    
    # Añadir datos POST si es una solicitud POST
    if request.method == 'POST':
        form_kwargs['data'] = request.POST
    
    # Añadir parámetros específicos según el tipo de sección
    if numero_seccion == 0:
        form_kwargs['user'] = request.user
    elif numero_seccion == 1:
        form_kwargs['user'] = request.user
        form_kwargs['grupo'] = grupo
    else:
        # Para secciones 2+, añadir la instancia si existe
        if numero_seccion > 1 and cpqol and 'attr' in seccion:
            form_kwargs['instance'] = getattr(cpqol, seccion['attr'].lower(), None)
    
    # Añadir parámetro edad para MovimientoForm (solo si la sección tiene 'attr' y es 'movimiento')
    if 'attr' in seccion and seccion['attr'] == "movimiento" and grupo == "familiar":
        form_kwargs['edad'] = request.session.get('edad_paciente')
    
    # Manejar la sección de resultados (no tiene formulario)
    if grupo == "familiar" and numero_seccion == 17:
        if cpqol and hasattr(cpqol, 'resultados'):
            try:
                resultados_data = cpqol.resultados 
                labels = list(resultados_data.keys())
                values = list(resultados_data.values())
            except AttributeError:
                labels = []
                values = []
        else:
            labels = []
            values = []
        form = None
    else:
        # Instanciar el formulario con todos los parámetros
        form = current_form(**form_kwargs)
    
    # Procesar solicitud POST
    if request.method == 'POST' and form is not None:
        if form.is_valid():
            if numero_seccion == 0:
                return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion + 1}')
            elif numero_seccion == 1:
                cpqol = form.save()
            elif (grupo == "profesional" and numero_seccion == 5) or (grupo == "familiar" and numero_seccion == 16):
                if 'attr' in seccion:
                    instance = form.save(cpqol, seccion['attr'].lower())
                    cpqol.completado = True
                    cpqol.save()

                if grupo == "profesional":
                    return redirect(reverse('home'))
                else:
                    return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion + 1}&codigo={cpqol.codigo}')
            else:
                if 'attr' in seccion:
                    instance = form.save(cpqol, seccion['attr'].lower())
                    # DEBUG: Imprimir información después de guardar
                    print(f"Sección {numero_seccion} guardada correctamente")
                    print(f"Instancia guardada: {instance}")
                    print(f"Atributo: {seccion['attr'].lower()}")
            
            if 'attr' in seccion and seccion.get('attr') == "paciente" and grupo == "familiar":
                request.session['edad_paciente'] = instance.edad
            
            return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion + 1}&codigo={cpqol.codigo}')
        else:
            # DEBUG: Imprimir errores del formulario
            print(f"Errores del formulario: {form.errors}")
            print(f"Datos del formulario: {form.data}")
    
    # Preparar datos para la plantilla
    context = {
        'form': form,
        'seccion': seccion,
        'total_secciones': total_secciones,
        'grupo': grupo,
        'cpqol': cpqol,
    }
    
    # Añadir labels y values para la sección de resultados
    if grupo == "familiar" and numero_seccion == 17:
        context['labels'] = labels
        context['values'] = values
        
    return render(request, "core/formulario.html", context)


def exportar_excel(request):
    modelo_resource = CpqolResource()
    dataset = modelo_resource.export(Cpqol.objects.all())
    response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="resultados.xlsx"'
    return response