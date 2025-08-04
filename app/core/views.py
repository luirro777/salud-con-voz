from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .resources import CpqolResource

from .forms import *

# Create your views here.
'''
@login_required
def vista_formulario(request):
    grupo = request.user.groups.first().name if request.user.groups.all() else "profesional"
    print(f"Grupo del usuario: {grupo}")

    # Obtenemos el número de sección y código desde la URL
    numero_seccion = int(request.GET.get('seccion', 0))
    codigo_from_url = request.GET.get('codigo') 

    cpqol = None # Inicializar cpqol a None    

    # **Lógica para obtener la instancia principal de CPQOL/CPQOLProfesional**
    # Esta lógica debe asegurar que 'cpqol' no sea None para secciones > 1
    if numero_seccion > 1: # Si estamos en una sección que requiere una instancia de CPQOL/CPQOLProfesional
        if not codigo_from_url:
            # Si no hay código en la URL, no podemos continuar. Redirige a la sección inicial.
            return redirect(reverse('cpqol') + '?seccion=0') 

        try:
            if grupo == "profesional":
                cpqol = CpqolProfesional.objects.get(user=request.user, codigo=codigo_from_url)
            else:
                cpqol = Cpqol.objects.get(user=request.user, codigo=codigo_from_url)
        except (Cpqol.DoesNotExist, CpqolProfesional.DoesNotExist): # Captura las excepciones específicas
            # Si el código no corresponde a un CPQOL/CPQOLProfesional existente para este usuario,
            # redirigir a la sección de código o mostrar un error.
            print(f"Error: No se encontró instancia de CPQOL para usuario {request.user} y código {codigo_from_url}")
            return redirect(reverse('cpqol') + '?seccion=1') # Redirige a la sección de código

    print(f"Instancia de cpqol (o CpqolProfesional): {cpqol}")

    # Definimos las secciones del formulario 
    secciones = [
        {'form': TerminosYCondicionesForm, 'nombre': "Términos y condiciones", 'subtitulo': ""},
        {'form': CodigoForm, 'nombre': "Código de participante", 'subtitulo': "Generación de código de identificación"},
    ]
    # Definimos las secciones según el grupo del usuario
    if grupo == "profesional":
        secciones.extend([
            {'form': ProfesionalForm, 'attr': "profesional", 'nombre': "Caracterización del profesional y el lugar de atención", 'subtitulo': "En esta sección deberá responder preguntas referidas a su profesión y el lugar en el cual atiende al NNAJ"},
            {'form': ContextoForm, 'attr': "contexto", "nombre": "Datos generales del NNAJ y su contexto", 'subtitulo': "La siguiente sección contiene algunas preguntas sobre el NNAJ y su contexto"},
            {'form': DatosClinicosForm, 'attr': "datos_clinicos", 'nombre': "Datos clínicos del NNAJ", 'subtitulo': "En la siguiente sección le preguntaremos por algunos datos clínicos relacionados a la salud del NNAJ, en particular relacionados a escalas que miden distintas funciones. Si por razón de incumbencia desconociera estos datos, por favor,intente ponerse en contacto con otro profesional que pudiera facilitarlos"},
            {'form': FinalizacionForm, 'attr': "finalizacion", 'nombre': "Finalizar cuestionario", 'subtitulo': "Agradecemos que se haya tomado el tiempo de completar estos cuestionarios que nos ayudan a conocer la calidad de vida de las infancias y juventudes con parálisis cerebral; si quisiera que nos comuniquemos con Ud. para continuar colaborando y conocer más sobre nuestro trabajo, por favor, escriba su dirección de correo electrónico"},
        ])
    else:
        secciones.extend([
            {'form': TutorForm, 'attr': "tutor", 'nombre': "Padre, madre o cuidador", 'subtitulo': 'Información general sobre la persona que responde'},
            {'form': PacienteForm, 'attr': "paciente", 'nombre': "Paciente", 'subtitulo': 'Datos generales de niño/a o adolescente'},
            {'form': MovimientoForm, 'attr': "movimiento", 'nombre': "Movilidad", 'subtitulo': 'Datos generales sobre la movilidad del niño/a o adolescente'},
            {'form': SentimientosForm, 'attr': "sentimientos", 'nombre': "Calidad de vida del niño/a o adolescente con parálisis cerebral", 'subtitulo': ""},
            {'form': RelacionesForm, 'attr': "relaciones", 'nombre': "Relaciones con los demás", 'subtitulo': ''},
            {'form': FamiliaForm, 'attr': "familia", 'nombre': "Familia", 'subtitulo': ''},
            {'form': ParticipacionForm, 'attr': "participacion", 'nombre': "Participacion", 'subtitulo': ''},
            {'form': EscuelaForm, 'attr': "escuela", 'nombre': "Escuela o Colegio", 'subtitulo': ''},
            {'form': SaludForm, 'attr': "salud", 'nombre': "Salud", 'subtitulo': ''},
            {'form': DolorForm, 'attr': "dolor", 'nombre': "Dolor y molestias", 'subtitulo': ''},
            {'form': ServiciosForm, 'attr': "servicios", 'nombre': "Acceso a servicios", 'subtitulo': ''},
            {'form': SaludUltimaSemanaForm, 'attr': "salud_ultima_semana", 'nombre': "Más preguntas sobre la salud del niño/a o adolescente", 'subtitulo': 'Las siguientes preguntas son similares a algunas que ya respondió; pero ahora, por favor, piense en la última semana.'},
            {'form': SaludUltimaSemana2Form, 'attr': "salud_ultima_semana_2", 'nombre': "Sobre la salud del chico o chica", 'subtitulo': 'Las preguntas a continuación corresponden a un cuestionario de salud que se aplica a cualquier niño/a o adolescente en cualquier situación (con o sin problemas de salud), por lo que pueden resultar difíciles de responder. Por favor, responda según lo mejor que usted conozca, asegurándose de que sus respuestas reflejen la perspectiva de su hijo/a. Trate de recordar las experiencias del chico/a durante la última semana.'},
            {'form': HogarForm, 'attr': "hogar", 'nombre': "Características del hogar", 'subtitulo': 'Esta es la última parte de la encuesta y le solicitamos que responda acerca de algunas características del hogar donde vive la chica o el chico. Estos datos son muy importantes para analizar a qué hogares hemos podido llegar con este estudio, para ofrecer información sobre la población argentina con parálisis cerebral (recuerde que estos datos nunca se analizan ni informan individualmente).'},
            {'form': None, 'nombre': "Informe de resultados", 'subtitulo': 'Calidad de vida relacionada con la salud en niñas, niños, adolescentes y jóvenes con parálisis cerebral'},
        ])

    total_secciones = len(secciones) - 1

    seccion = secciones[numero_seccion]
    seccion['numero'] = numero_seccion
    seccion['siguiente'] = numero_seccion + 1
    if numero_seccion > 1:
        seccion['anterior'] = numero_seccion - 1
    seccion['grupo'] = grupo

    current_form = seccion['form']

    if request.method == 'POST': # POST request
        # Instancia el formulario con los datos POST
        if numero_seccion == 0: # TerminosYCondicionesForm
            form = current_form(request.user, data=request.POST)
        elif numero_seccion == 1: # CodigoForm
            form = current_form(request.user, grupo=grupo, data=request.POST)
        else:
            # Para secciones > 1, necesitamos la instancia cpqol al inicializar el formulario.            
            form = current_form(instance=getattr(cpqol, seccion['attr'].lower(), None), data=request.POST)
        
        # Logica una vez verificado el formulario
        if form.is_valid():
            if numero_seccion == 0: # Términos y condiciones
                return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion + 1}')
            elif numero_seccion == 1: # Código (crea el CPQOL/CPQOLProfesional)
                cpqol = form.save() # Aquí se crea y se asigna a 'cpqol'
            elif grupo == "profesional" and numero_seccion == 5:
                instance = form.save(cpqol, seccion['attr'].lower())                
                return redirect(reverse('home'))
            else: # Resto de secciones, guardan en la instancia existente                
                instance = form.save(cpqol, seccion['attr'].lower())
            
            # Guardar la edad en la sesión si es el PacienteForm            
            if grupo == "familiar" and seccion.get('attr') == "paciente":                
                request.session['edad_paciente'] = instance.edad

            return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion + 1}&codigo={cpqol.codigo}')

    else: # GET request
        print(f"el total de secciones es: {total_secciones}")
        if not numero_seccion == 16:
            if numero_seccion > 1:
                # Al inicializar el formulario en GET, recupera la instancia asociada si existe
                instance = getattr(cpqol, seccion['attr'].lower(), None)
                if grupo == "familiar" and seccion['attr'] == "movimiento": # MovimientoForm
                    print(f"Recuperando de sesión: {request.session.get('edad_paciente')}")
                    edad = request.session.get('edad_paciente')
                    try:
                        edad = int(edad)
                    except (ValueError, TypeError):
                        edad = None
                    form = current_form(edad=edad, instance=instance)
                else:
                    form = current_form(instance=instance)                    
            else:
                # Formulario para la sección 0 o 1
                if numero_seccion == 1: # CodigoForm
                    form = current_form(request.user, grupo=grupo)
                else: # TerminosYCondicionesForm (seccion 0)
                    form = current_form(request.user)
            

    # Si es la última sección, mostrar los resultados
    if grupo == "familiar" and numero_seccion == 16:
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
    
    return render(request, "core/formulario.html", locals())


'''
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
        {'form': TerminosYCondicionesForm, 'nombre': "Términos y condiciones", 'subtitulo': ""},
        {'form': CodigoForm, 'nombre': "Código de participante", 'subtitulo': "Generación de código de identificación"},
    ]
    # Definimos las secciones según el grupo del usuario
    if grupo == "profesional":
        secciones.extend([
            {'form': ProfesionalForm, 'attr': "profesional", 'nombre': "Caracterización del profesional y el lugar de atención", 'subtitulo': "En esta sección deberá responder preguntas referidas a su profesión y el lugar en el cual atiende al NNAJ"},
            {'form': ContextoForm, 'attr': "contexto", "nombre": "Datos generales del NNAJ y su contexto", 'subtitulo': "La siguiente sección contiene algunas preguntas sobre el NNAJ y su contexto"},
            {'form': DatosClinicosForm, 'attr': "datos_clinicos", 'nombre': "Datos clínicos del NNAJ", 'subtitulo': "En la siguiente sección le preguntaremos por algunos datos clínicos relacionados a la salud del NNAJ, en particular relacionados a escalas que miden distintas funciones. Si por razón de incumbencia desconociera estos datos, por favor,intente ponerse en contacto con otro profesional que pudiera facilitarlos"},
            {'form': FinalizacionForm, 'attr': "correo", 'nombre': "Finalizar cuestionario", 'subtitulo': "Agradecemos que se haya tomado el tiempo de completar estos cuestionarios que nos ayudan a conocer la calidad de vida de las infancias y juventudes con parálisis cerebral; si quisiera que nos comuniquemos con Ud. para continuar colaborando y conocer más sobre nuestro trabajo, por favor, escriba su dirección de correo electrónico"},
        ])
    else:
        secciones.extend([
            {'form': TutorForm, 'attr': "tutor", 'nombre': "Padre, madre o cuidador", 'subtitulo': 'Información general sobre la persona que responde'},
            {'form': PacienteForm, 'attr': "paciente", 'nombre': "Paciente", 'subtitulo': 'Datos generales de niño/a o adolescente'},
            {'form': MovimientoForm, 'attr': "movimiento", 'nombre': "Movilidad", 'subtitulo': 'Datos generales sobre la movilidad del niño/a o adolescente'},
            {'form': SentimientosForm, 'attr': "sentimientos", 'nombre': "Calidad de vida del niño/a o adolescente con parálisis cerebral", 'subtitulo': ""},
            {'form': RelacionesForm, 'attr': "relaciones", 'nombre': "Relaciones con los demás", 'subtitulo': ''},
            {'form': FamiliaForm, 'attr': "familia", 'nombre': "Familia", 'subtitulo': ''},
            {'form': ParticipacionForm, 'attr': "participacion", 'nombre': "Participacion", 'subtitulo': ''},
            {'form': EscuelaForm, 'attr': "escuela", 'nombre': "Escuela o Colegio", 'subtitulo': ''},
            {'form': SaludForm, 'attr': "salud", 'nombre': "Salud", 'subtitulo': ''},
            {'form': DolorForm, 'attr': "dolor", 'nombre': "Dolor y molestias", 'subtitulo': ''},
            {'form': ServiciosForm, 'attr': "servicios", 'nombre': "Acceso a servicios", 'subtitulo': ''},
            {'form': SaludUltimaSemanaForm, 'attr': "salud_ultima_semana", 'nombre': "Más preguntas sobre la salud del niño/a o adolescente", 'subtitulo': 'Las siguientes preguntas son similares a algunas que ya respondió; pero ahora, por favor, piense en la última semana.'},
            {'form': SaludUltimaSemana2Form, 'attr': "salud_ultima_semana_2", 'nombre': "Sobre la salud del chico o chica", 'subtitulo': 'Las preguntas a continuación corresponden a un cuestionario de salud que se aplica a cualquier niño/a o adolescente en cualquier situación (con o sin problemas de salud), por lo que pueden resultar difíciles de responder. Por favor, responda según lo mejor que usted conozca, asegurándose de que sus respuestas reflejen la perspectiva de su hijo/a. Trate de recordar las experiencias del chico/a durante la última semana.'},
            {'form': HogarForm, 'attr': "hogar", 'nombre': "Características del hogar", 'subtitulo': 'Esta es la última parte de la encuesta y le solicitamos que responda acerca de algunas características del hogar donde vive la chica o el chico. Estos datos son muy importantes para analizar a qué hogares hemos podido llegar con este estudio, para ofrecer información sobre la población argentina con parálisis cerebral (recuerde que estos datos nunca se analizan ni informan individualmente).'},
            {'form': None, 'nombre': "Informe de resultados", 'subtitulo': 'Calidad de vida relacionada con la salud en niñas, niños, adolescentes y jóvenes con parálisis cerebral'},
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
        
        # Logica una vez verificado el formulario
        if form.is_valid(): # Secciones de TyC y código
            if numero_seccion == 0:
                return HttpResponseRedirect(reverse('cpqol') + f'?seccion={numero_seccion + 1}')
            elif numero_seccion == 1:
                cpqol = form.save()
            
            # lógica de finalización
            elif (grupo == "profesional" and numero_seccion == 5) or (grupo == "familiar" and numero_seccion == 15):
    
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
        elif grupo == "familiar" and numero_seccion == 16:
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
                elif numero_seccion == 16: # Resultados
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

def exportar_excel(request):
    modelo_resource = CpqolResource()
    dataset = modelo_resource.export(Cpqol.objects.filter(user=request.user))
    response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="resultados.xlsx"'
    return response