from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

#@admin.site.register(User)
class UserAdmin(UserAdmin):
    pass
# Register your models here.
admin.site.register(Estudiante)
admin.site.register(Profesor)
#admin.site.register(User)
admin.site.register(Clase)
admin.site.register(Pago)
admin.site.register(Promociones)
admin.site.register(Inscripcion)
admin.site.register(Curso)
admin.site.register(User, UserAdmin)
admin.site.register(Compra)
admin.site.register(Tarea)

admin.site.register(Sesion)
admin.site.register(Supervisor)
admin.site.register(Asistencia)
admin.site.register(Deber)
admin.site.register(TCP)