from .views import *
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet,FCMDeviceViewSet
urlpatterns = [
    path('auth/register/user',RegisterUserAPI.as_view()),

    path('auth/login/user',CustomAuthToken.as_view()),

    path('auth/register/profesor',RegisterProfesorAPI.as_view()),
 path('auth/register/supervisor',RegisterSupervisorAPI.as_view()),
    path('cursos',CursoGet.as_view()),
    path('createtoken',FCMDeviceAuthorizedViewSet.as_view({'post': 'create'})),
path('curso/<str:pk>',GetCurso.as_view()),path('crearPago',CreatePago.as_view()),
path('getClase/<str:id>',ClaseGet.as_view()),path('getTarea',TareaGet.as_view()),
#path('getTarea/estudiante/',TareaFilter.as_view(),name="Filter Tarea"),
path('getPromo',PromoGet.as_view())
,path('crearClase',CreateClase.as_view()),
path('crearPromo',PromoSave.as_view()),
path('sendnotificacion', SendNotificacion.as_view(),name='Send Notificacion'),

path('getcompras/<str:id>',getCompras.as_view()),
path('crearpago',CreatePago.as_view()),
path('crearcompra',CreateCompra.as_view()),
path('getcursosprofesor/<str:id>',getCursosbyProfesor.as_view()),
path('creartarea',CreateTarea.as_view()),   #CREAR TAREA POR PROFESOR
path('crearsesion',CreateSesion.as_view()),
path('asistencia',updateAsistencia.as_view()),
path('checkasistencia',checkAsistencia.as_view()),
path('updateclase/<int:pk>',UpdateClase.as_view()),

path('getasistencias/<int:id>',AsistenciabySesion.as_view()),

path('getTarea/<int:pk>',GetTarea.as_view()),
path('getprofesor/<str:pk>',GetProfesor.as_view()),
path('getsesion/<int:pk>',GetSesion.as_view()),

path('listcalificacion/<int:id>',listTareaCalificacion.as_view()),   #LISTA CALIFICACIONES
path('calificar',asignarCalificacion.as_view()),  #ASIGNA CALIFICACION  listSesiones
path('sesiones/<int:id>',listSesiones.as_view()),
path('listtareas/<str:ide>/<int:idt>',listTareas.as_view()),  #muestra la tarea de un estudiante
path('alltareas/<int:id>',getAllTareas.as_view()),
path('eliminartarea',eliminarTarea.as_view()),
path('gettareas/<str:id>/<int:idt>',getAllTareasEstudiante.as_view()),
path('gettasistencias/<str:id>/<int:idt>',getAllAsistenciasEstudiante.as_view()),
path('getclasessupervisor/<str:id>',getClasesSupervisor.as_view()),
path('getsupervisor/<str:pk>',GetSupervisor.as_view()),
path('getclase/<int:pk>',GetClase.as_view()),

path('estudiante/update/<str:pk>',UpdateEstudiante.as_view()),   #modificar estudiantes
path('profesor/update/<str:pk>',UpdateProfesor.as_view()),
path('supervisor/update/<str:pk>',UpdateSupervisor.as_view()),
path('getstudent/<str:pk>',GetStuden.as_view()),
path('getstudents',EstudianteAll.as_view()),
path('getsupervisores',SupervisorAll.as_view()),
path('getprofesores',ProfesorAll.as_view()),
path('sendnotificacionbycurso', SendNotificacionbyCurso.as_view(),name='Send Notificacion'),
path('sendnotificacionbygrupo', SendNotificacionbyTipo.as_view(),name='Send Notificacion'),
path('createpaquet',TcpNew.as_view()),
path('getpaquet',TcpGet.as_view()),
path('pruebacache',view_books),
path('redis',view_cached_books),


]
#path('getestudiantes/<str:id>',getEstudiantesbyCursos.as_view()),


