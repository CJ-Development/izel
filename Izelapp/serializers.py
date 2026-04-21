from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    Usuario, Paciente, Medico, Administrador,
    Consulta, Cita, Disponibilidad,
    RecetaMedica, OrdenMedica, CertificadoIncapacidad,
    PerfilPaciente, TablaReferenciaCIE10
)


# ─── Autenticación ────────────────────────────────────────────────────────────

class LoginSerializer(serializers.Serializer):
    tipo_doc = serializers.CharField()
    username = serializers.CharField()  # num_doc
    password = serializers.CharField(write_only=True)
 
    def validate(self, data):
        tipo_doc = data.get('tipo_doc')
        username = data.get('username')
        password = data.get('password')
 
        # Paso 1 — Verifica que el usuario existe
        try:
            usuario_obj = Usuario.objects.get(num_doc=username)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError('Credenciales incorrectas.')
 
        # Paso 2 — Verifica que el tipo de documento coincide
        if usuario_obj.tipo_doc != tipo_doc:
            raise serializers.ValidationError('El tipo de documento no coincide.')
 
        # Paso 3 — Verifica contraseña
        usuario = authenticate(username=username, password=password)
        if not usuario:
            raise serializers.ValidationError('Credenciales incorrectas.')
 
        # Paso 4 — Verifica que está activo
        if not usuario.is_active:
            raise serializers.ValidationError('Usuario inactivo. Contacta al administrador.')
 
        data['usuario'] = usuario
        return data
 

# ─── Usuario base ─────────────────────────────────────────────────────────────

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono',
            'fecha_nacimiento', 'tipo_poblacion', 'ocupacion', 'eps', 'imagen'
        ]
        read_only_fields = ['id']


# ─── Paciente ─────────────────────────────────────────────────────────────────

class PacienteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Paciente
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono',
            'fecha_nacimiento', 'tipo_poblacion', 'ocupacion', 'eps',
            'imagen', 'regimen', 'password'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        paciente = Paciente(**validated_data)
        if password:
            paciente.set_password(password)
        paciente.save()
        return paciente

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# ─── Médico ───────────────────────────────────────────────────────────────────

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono',
            'fecha_nacimiento', 'tipo_poblacion', 'ocupacion', 'eps',
            'imagen', 'especialidad', 'numero_registro_profesional',
            'licencia_certificacion', 'fecha_contratacion'
        ]
        read_only_fields = ['id']


class MedicoResumenSerializer(serializers.ModelSerializer):
    """Versión ligera para listas y selects"""
    class Meta:
        model = Medico
        fields = ['id', 'first_name', 'last_name', 'especialidad', 'imagen']


# ─── Administrador ────────────────────────────────────────────────────────────

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'tipo_doc', 'num_doc', 'genero', 'rh', 'telefono',
            'fecha_nacimiento', 'tipo_poblacion', 'ocupacion', 'eps',
            'imagen', 'rol_acceso', 'centro_administracion'
        ]
        read_only_fields = ['id']


# ─── Disponibilidad ───────────────────────────────────────────────────────────

class DisponibilidadSerializer(serializers.ModelSerializer):
    medico_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Disponibilidad
        fields = [
            'id', 'medico', 'medico_nombre', 'fecha',
            'hora_inicio', 'hora_fin', 'tipo_cita',
            'estado', 'max_pacientes', 'duracion'
        ]

    def get_medico_nombre(self, obj):
        return f"{obj.medico.first_name} {obj.medico.last_name}"


# ─── Cita ─────────────────────────────────────────────────────────────────────

class CitaSerializer(serializers.ModelSerializer):
    medico_nombre = serializers.SerializerMethodField()
    paciente_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        fields = [
            'id', 'fecha_cita', 'hora_cita', 'estado_cita',
            'especialidad', 'medico', 'medico_nombre',
            'paciente', 'paciente_nombre', 'disponibilidad'
        ]

    def get_medico_nombre(self, obj):
        return f"{obj.medico.first_name} {obj.medico.last_name}"

    def get_paciente_nombre(self, obj):
        return f"{obj.paciente.first_name} {obj.paciente.last_name}"


# ─── Consulta ─────────────────────────────────────────────────────────────────

class ConsultaSerializer(serializers.ModelSerializer):
    medico_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Consulta
        fields = [
            'id', 'especialidad', 'tratamiento',
            'diagnostico_principal', 'diagnostico_relacionado',
            'motivo_consulta', 'fecha_consulta',
            'medico', 'medico_nombre', 'paciente'
        ]
        read_only_fields = ['fecha_consulta']

    def get_medico_nombre(self, obj):
        return f"{obj.medico.first_name} {obj.medico.last_name}"


# ─── Receta Médica ────────────────────────────────────────────────────────────

class RecetaMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetaMedica
        fields = [
            'id', 'medico', 'paciente', 'medicamento',
            'concentracion', 'duracion', 'cantidad',
            'via_administracion', 'intervalo', 'recomendaciones',
            'indicaciones', 'fecha_medicado',
            'diagnostico_principal', 'diagnostico_relacionado'
        ]


# ─── Orden Médica ─────────────────────────────────────────────────────────────

class OrdenMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenMedica
        fields = [
            'id', 'cups', 'medico', 'paciente',
            'especialidad_referido', 'cantidad',
            'diagnostico_principal', 'diagnostico_relacionado',
            'motivo', 'fecha_ordenado', 'vigencia', 'estado'
        ]
        read_only_fields = ['fecha_ordenado']


# ─── Certificado de Incapacidad ───────────────────────────────────────────────

class CertificadoIncapacidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificadoIncapacidad
        fields = [
            'id', 'medico', 'paciente', 'dias_incapacidad',
            'motivo_incapacidad', 'fecha_inicio', 'fecha_fin',
            'diagnostico_principal', 'diagnostico_relacionado', 'observaciones'
        ]


# ─── Perfil Paciente ──────────────────────────────────────────────────────────

class PerfilPacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilPaciente
        fields = '__all__'


# ─── CIE10 ───────────────────────────────────────────────────────────────────

class CIE10Serializer(serializers.ModelSerializer):
    class Meta:
        model = TablaReferenciaCIE10
        fields = ['id', 'codigo', 'nombre', 'descripcion']
