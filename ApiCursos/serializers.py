from .models import *

from rest_framework import serializers

from django.contrib.auth import authenticate

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Estudiante
        model = Estudiante
        fields = ('nombres','apellidos','cedula','fecha_nacimiento','direccion', 'telefono',
                            'escolaridad', 'pais', 'ciudad','sexo','grupo_excluido','estado')

class ProfesorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Profesor
        model = Profesor
        fields = ('nombres','apellidos','cedula','fecha_nacimiento','direccion', 'telefono',
                            'escolaridad', 'pais', 'ciudad','sexo','estado')



class SupervisorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Supervisor
        model = Supervisor
        fields = ('nombres','apellidos','cedula','fecha_nacimiento','direccion', 'telefono',
                            'escolaridad', 'pais', 'ciudad','sexo','estado')


class UserSerializerSupervisor(serializers.ModelSerializer):
    profile = SupervisorProfileSerializer(required=True)
    #url = serializers.HyperlinkedIdentityField(view_name="ApiCursos:user-detail")
    class Meta:
        model = User
        fields = ('email', 'password','rol','profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Supervisor.objects.create(user=user, **profile_data)
        return user

class UserSerializerProfesor(serializers.ModelSerializer):
    profile = ProfesorProfileSerializer(required=True)
    #url = serializers.HyperlinkedIdentityField(view_name="ApiCursos:user-detail")
    class Meta:
        model = User
        fields = ('email', 'password','rol','profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profesor.objects.create(user=user, **profile_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=True)
    #url = serializers.HyperlinkedIdentityField(view_name="ApiCursos:user-detail")
    class Meta:
        model = User
        fields = ('email', 'password','rol','profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Estudiante.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()
        profile.nombres = profile_data.get('nombres', profile.nombres)
        profile.apellidos = profile_data('apellidos',profile.apellidos)
        profile.fecha_nacimiento = profile_data('fecha_nacimiento',profile.fecha_nacimiento)
        #profile.photo = profile_data.get('photo', profile.photo)
        profile.cedula = profile_data('cedula',profile.cedula)
        #profile.dob = profile_data.get('dob', profile.dob)
        profile.direccion = profile_data.get('direccion', profile.direccion)
        profile.telefono = profile_data.get('telefono', profile.telefono)
        profile.escolaridad  = profile_data.get('escolaridad', profile.escolaridad )
        profile.pais = profile_data.get('pais', profile.pais)
        profile.ciudad = profile_data.get('ciudad', profile.ciudad)
        profile.grupo_excluido = profile_data.get('grupo_excluido', profile.grupo_excluido)
        profile.sexo = profile_data.get('sexo', profile.sexo)
        profile.save()

        return instance






class CursoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Curso
        fields = "__all__"


class PagoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pago
        fields = "__all__"



class ClaseSerializer(serializers.ModelSerializer):
    id_curso = CursoSerializer(required = True)
    class Meta:
        model = Clase
        fields = ('id','titulo','id_curso','id_supervisor')


class ClaseSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = ('id_curso','id_estudiante')
        depth = 1



class Compra2Serializer(serializers.ModelSerializer):

    class Meta:
        model = Compra
        fields = "__all__"



class SesionSerializerMod(serializers.ModelSerializer):

      class Meta:
            model =  Sesion
            fields = ['id','titulo']

class ProfesorSerializerMod(serializers.ModelSerializer):

      class Meta:
            model =  Profesor
            fields = ('nombres','apellidos')


class TareaSerializer(serializers.ModelSerializer):
    id_sesion = SesionSerializerMod()
    id_profesor = ProfesorSerializerMod()
    class Meta:
        model = Tarea
        fields = ('id','estado','nombre_tarea','descripcion_tarea','id_profesor','id_sesion','fecha_creacion','url','fecha_entrega')

class PromoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promociones
        fields = "__all__"

class TareaSerial(serializers.ModelSerializer):

    class Meta:
        model = Tarea
        fields = "__all__"




class ClaseUpdate(serializers.ModelSerializer):
    id_estudiante = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Estudiante.objects.all())

    class Meta:
        model = Clase
        fields = ('id_profesor','id_curso', 'id_estudiante')

    def update(self, instance, validated_data):
        subjects = validated_data.pop('id_estudiante')

        teacher = instance
        print(subjects)
        print(teacher)

        for subject in subjects:
            teacher.id_estudiante.add(subject)


        teacher.save()

        return teacher




class CompraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Compra
        fields = ['id_curso']
        depth = 1





class SesionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sesion
        fields = "__all__"


class ResultStudentSerializer(serializers.ModelSerializer):

      class Meta:
            model =  Estudiante
            fields = ('nombres','apellidos','cedula')
            #exclude = ('address',)

class AsistenciaSerializer(serializers.ModelSerializer):


    class Meta:
        model = Asistencia
        fields = ('id_estudiante','asistencia','asistido')
        depth = 1




class CalificacionSerializer(serializers.ModelSerializer):
    id_estudiante =  ResultStudentSerializer()

    class Meta:
        model = Deber
        fields = ('id_estudiante','estado','calificacion')
        depth = 1




class DeberSerializer(serializers.ModelSerializer):
    id_estudiante =  ResultStudentSerializer()

    class Meta:
        model = Deber
        fields = ('calificacion','id_tarea','id_estudiante')
        depth = 1


class ResultClaseSerializer(serializers.ModelSerializer):

      class Meta:
            model =  Clase
            fields = ['titulo']




class ResultSesionSerializer(serializers.ModelSerializer):
      id_clase = ResultClaseSerializer()
      class Meta:
            model =  Sesion
            fields = ['id_clase']
            depth = 1


class ResultTareaSerializer(serializers.ModelSerializer):
      id_sesion = ResultSesionSerializer()
      class Meta:
            model =  Tarea
            fields = ('nombre_tarea','id_sesion')
            depth = 2


class DeberSerializerMovil(serializers.ModelSerializer):

    id_tarea = ResultTareaSerializer()

    class Meta:
        model = Deber
        fields = ('calificacion','id_tarea')
        depth = 1


class ResultSesionSerializerMovil(serializers.ModelSerializer):
      id_clase = ResultClaseSerializer()
      class Meta:
            model =  Sesion
            fields = ('titulo','id_clase')
            depth = 1

class AsistenciaserializerMovil(serializers.ModelSerializer):

    id_sesion = ResultSesionSerializerMovil()

    class Meta:
        model = Asistencia
        fields = ('asistencia','id_sesion')
        depth = 1

class ClaseSerializerAll(serializers.ModelSerializer):

    class Meta:
        model = Clase
        fields = ('id','titulo','id_curso','id_estudiante','id_profesor')
        depth = 1


class Tcpserializer(serializers.ModelSerializer):

    class Meta:
        model = TCP
        fields = "__all__"
