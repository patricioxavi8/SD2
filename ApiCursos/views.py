from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response
# Also add these imports
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.permissions import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from fcm_django.models import FCMDevice
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)



class CustomAuthToken(ObtainAuthToken):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        cedula = None
        nombre = None
        apellido = None

        try:
            profesor = Profesor.objects.get(user=user)
        except Profesor.DoesNotExist:
            profesor = None
        try:
            estudiante = Estudiante.objects.get(user=user)
        except Estudiante.DoesNotExist:
            estudiante = None
        try:
            supervisor = Supervisor.objects.get(user=user)
        except Supervisor.DoesNotExist:
            supervisor = None
        if profesor:
            cedula = profesor.cedula
            nombre = profesor.nombres
            apellido = profesor.apellidos
        if estudiante:
            cedula = estudiante.cedula
            nombre = estudiante.nombres
            apellido = estudiante.apellidos
        if supervisor:
            cedula = supervisor.cedula
            nombre = supervisor.nombres
            apellido = supervisor.apellidos




        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'isAdmin': user.is_superuser,
            'cedula': cedula,
            'rol': user.rol,
            'nombre' : nombre ,
            'apellido' : apellido


        })



class RegisterUserAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,

        })

class RegisterProfesorAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializerProfesor

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializerProfesor(user, context=self.get_serializer_context()).data,

        })


class RegisterSupervisorAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializerSupervisor

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializerSupervisor(user, context=self.get_serializer_context()).data,

        })




class CursoGet(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class GetCurso(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class CreatePago(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer



class ClaseGet(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ClaseSerializer


    def get_queryset(self):
        filtro = self.kwargs['id']
        queryset = Clase.objects.filter(id_estudiante=filtro)
        return  queryset

class TareaGet(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

class TareaFilter(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TareaSerializer


    def get_queryset(self):


        filtro =self.request.GET.get('id_clase')
        filtro2 =self.request.GET.get('id_estudiante')

        queryset = Tarea.objects.filter(id_clase__id_estudiante=filtro2,id_clase__id_curso=filtro)

        return  queryset

class PromoGet(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Promociones.objects.all()
    serializer_class = PromoSerializer



class CreateClase(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer2

class PromoSave(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Promociones.objects.all()
    serializer_class = PromoSerializer


class SendNotificacion(APIView):
    permission_classes =(AllowAny,)
    def post(self, request,format='json'):
        if(request.method=='POST'):
            titulo = request.data['titulo']
            body = request.data['body']

            devices = FCMDevice.objects.all()

            devices.send_message(title=titulo, body=body)

            return Response(request.data)









class getCompras(generics.ListAPIView):

    permission_classes = (AllowAny,)
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    def get_queryset(self):

        filtro = self.kwargs['id']
        queryset = Compra.objects.filter(id_estudiante=filtro)
        return  queryset

class CreatePago(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class CreateCompra(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Compra.objects.all()
    serializer_class = Compra2Serializer



### CURSOS POR PROFESOR
class getCursosbyProfesor(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ClaseSerializer2


    def get_queryset(self):
        filtro = self.kwargs['id']
        queryset = Clase.objects.filter(id_profesor=filtro)
        return  queryset


class CreateTarea(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Tarea.objects.all()
    serializer_class = TareaSerial



class CreateSesion(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer


####ASIGNA ASISTENCIA
class updateAsistencia(APIView):
    permission_classes =(AllowAny,)
    def patch(self, request,format='json'):
        if(request.method=='PATCH'):

            sesion = request.data['id_sesion']
            student = request.data['id_estudiante']
            asis = request.data['asistencia']
            asisti = request.data['asistido']
            Asistencia.objects.filter(id_sesion__id=sesion,id_estudiante=student).update(asistencia=asis,asistido=asisti)

            #asistencia = Asistencia.objects.get(id_sesion__id=sesion, id_estudiante=student)

            return Response(request.data)


#CONSULTA ASISTENCIA DE UN ESTUDIANTE
class checkAsistencia(APIView):
    permission_classes =(AllowAny,)
    def get(self, request,format='none'):
        if(request.method=='GET'):

            sesion = request.data['id_sesion']
            student = request.data['id_estudiante']


            asistencia = Asistencia.objects.get(id_sesion__id=sesion, id_estudiante=student)

            return Response({'Estado':asistencia.asistencia})




# actualiza la tabla clase
class UpdateClase(generics.UpdateAPIView):

    permission_classes = (AllowAny,)
    queryset = Clase.objects.all()
    serializer_class = ClaseUpdate


# obtiene las asistencias por una sesion

class AsistenciabySesion(generics.ListAPIView):

    permission_classes = (AllowAny,)

    serializer_class = AsistenciaSerializer


    def get_queryset(self):
        filtro = self.kwargs['id']
        queryset = Asistencia.objects.filter(id_sesion=filtro).order_by('id_estudiante__apellidos')
        return  queryset


#OBTIENE LA INFORMACION DE UNA TAREA
class GetTarea(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    serializer_class = TareaSerializer


    def get_queryset(self):

        queryset = Tarea.objects.filter(estado=True)
        return  queryset



#LISTAR CALIFICACIONES DE UNA TAREA
class listTareaCalificacion(generics.ListAPIView):

    permission_classes = (AllowAny,)

    serializer_class = CalificacionSerializer


    def get_queryset(self):
        filtro = self.kwargs['id']
        queryset = Deber.objects.filter(id_tarea=filtro,id_tarea__estado=True).order_by('id_estudiante__apellidos')
        return  queryset



##CALIFICA LAS TAREAS
class asignarCalificacion(APIView):
    permission_classes =(AllowAny,)
    def patch(self, request,format='json'):
        if(request.method=='PATCH'):
            calificacion = request.data['calificacion']
            sesion = request.data['id_tarea']
            student = request.data['id_estudiante']
            Deber.objects.filter(id_tarea__id=sesion,id_estudiante=student).update(calificacion=calificacion,estado=True)



            return Response(request.data)








# listar todas las sesiones de una clase

class listSesiones(generics.ListAPIView):

    permission_classes = (AllowAny,)

    serializer_class = SesionSerializer


    def get_queryset(self):
        filtro = self.kwargs['id']
        queryset = Sesion.objects.filter(id_clase=filtro)
        return  queryset




#Obtener Tarea de un estudiante
class listTareas(generics.ListAPIView):

    permission_classes = (AllowAny,)

    serializer_class = DeberSerializer


    def get_queryset(self):
        filtro = self.kwargs['ide']
        filtro2 = self.kwargs['idt']
        queryset = Deber.objects.filter(id_estudiante=filtro,id_tarea__estado=True).filter(id_tarea=filtro2)
        return  queryset



##OBTIENE TODAS LAS TAREAS DE UN CURSO

class getAllTareas(generics.ListAPIView):

    permission_classes = (AllowAny,)

    serializer_class = TareaSerializer


    def get_queryset(self):
        filtro = self.kwargs['id']

        queryset = Tarea.objects.filter(id_sesion__id_clase=filtro,estado=True)
        return  queryset




##ELIMINAR TAREA

class eliminarTarea(APIView):
    permission_classes =(AllowAny,)
    def patch(self, request,format='json'):
        if(request.method=='PATCH'):

            tarea = request.data['id_tarea']
            Tarea.objects.filter(id=tarea).update(estado=False)



            return Response(request.data)



class GetProfesor(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Profesor.objects.all()
    serializer_class = ProfesorProfileSerializer


class GetSesion(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer


class getAllTareasEstudiante(generics.ListAPIView):

    permission_classes = (AllowAny,)

    serializer_class = DeberSerializerMovil


    def get_queryset(self):
        filtro = self.kwargs['id']
        filtro2 = self.kwargs['idt']
        queryset = Deber.objects.filter(id_estudiante=filtro,id_tarea__id_sesion__id_clase=filtro2)
        return  queryset


class getAllAsistenciasEstudiante(generics.ListAPIView):

    permission_classes = (AllowAny,)

    serializer_class = AsistenciaserializerMovil


    def get_queryset(self):
        filtro = self.kwargs['id']
        filtro2 = self.kwargs['idt']
        queryset = Asistencia.objects.filter(id_estudiante=filtro,id_sesion__id_clase=filtro2)
        return  queryset



class getClasesSupervisor(generics.ListAPIView):  #todas las clases de un supervisor

    permission_classes = (AllowAny,)

    serializer_class = ClaseSerializer


    def get_queryset(self):
        filtro = self.kwargs['id']

        queryset = Clase.objects.filter(id_supervisor=filtro)
        return  queryset

class GetSupervisor(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Supervisor.objects.all()
    serializer_class = SupervisorProfileSerializer


class GetClase(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializerAll



class UpdateEstudiante(generics.UpdateAPIView):

    permission_classes = (AllowAny,)
    queryset = Estudiante.objects.all()
    serializer_class = UserProfileSerializer


class UpdateProfesor(generics.UpdateAPIView):

    permission_classes = (AllowAny,)
    queryset = Profesor.objects.all()
    serializer_class = ProfesorProfileSerializer


class UpdateSupervisor(generics.UpdateAPIView):

    permission_classes = (AllowAny,)
    queryset = Supervisor.objects.all()
    serializer_class = SupervisorProfileSerializer

class GetStuden(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Estudiante.objects.all()
    serializer_class = UserProfileSerializer



class EstudianteAll(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Estudiante.objects.filter(estado=True)
    serializer_class = UserProfileSerializer

class SupervisorAll(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Supervisor.objects.filter(estado=True)
    serializer_class = SupervisorProfileSerializer

class ProfesorAll(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Profesor.objects.filter(estado=True)
    serializer_class = ProfesorProfileSerializer


class SendNotificacionbyCurso(APIView):
    permission_classes =(AllowAny,)
    def post(self, request,format='json'):
        if(request.method=='POST'):
            titulo = request.data['titulo']
            body = request.data['body']
            id_clase = request.data['id_clase']


            valor = Clase.objects.get(id=id_clase)
            pruebita =  valor.id_estudiante.values_list('user_id')
            devices = FCMDevice.objects.filter(user_id__in= pruebita)
            devices.send_message(title=titulo, body=body)

            return Response(request.data)


class SendNotificacionbyTipo(APIView):
    permission_classes =(AllowAny,)
    def post(self, request,format='json'):
        if(request.method=='POST'):
            titulo = request.data['titulo']
            body = request.data['body']
            grupo = request.data['grupo']


            devices = FCMDevice.objects.filter(user_id__in=User.objects.filter(profile__grupo_excluido=grupo))
            devices.send_message(title=titulo, body=body)

            return Response(request.data)

'''class getEstudiantesbyCursos(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ClaseSerializer3


    def get_queryset(self):
        filtro = self.kwargs['id']
        queryset = Clase.objects.filter(id_curso=filtro)
        return  queryset    '''



class TcpNew(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = TCP.objects.all()
    serializer_class = Tcpserializer

class TcpGet(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = TCP.objects.all()
    serializer_class = Tcpserializer

    
@api_view(['GET'])
@permission_classes([AllowAny])
def view_books(request):
    
    products = Estudiante.objects.all()
    results = [product.to_json() for product in products]
    return Response(results, status=status.HTTP_201_CREATED)



@api_view(['GET'])
@permission_classes([AllowAny])
def view_cached_books(request):

    if 'estudiante' in cache:
        # se obtienen resultados si esta en caché
        products = cache.get('estudiante')
        return Response(products, status=status.HTTP_201_CREATED)
 
    else:
        products = Estudiante.objects.all()
        results = [product.to_json() for product in products]
        # Se almacenan datos en caché
        cache.set('estudiante', results, timeout=CACHE_TTL)
        return Response(results, status=status.HTTP_201_CREATED)
