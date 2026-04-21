from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.exceptions import ValidationError
import logging
import os

logger = logging.getLogger(__name__)

# ─── Una sola definición (eliminada la duplicada) ─────────────────────────────
def ruta_directorio_usuario(instance, filename):
    return f'usuarios/{instance.username}/{filename}'


# region Usuario
class Usuario(AbstractUser):
    OPCIONES_TIPODOC = [
        ('CC',  'Cédula de Ciudadanía'),
        ('CE',  'Cédula de Extranjería'),
        ('NIT', 'NIT'),
        ('PPT', 'Permiso de Protección Temporal'),
    ]
    GENERO_OPCIONES = [
        ('masculino',          'MASCULINO'),
        ('femenino',           'FEMENINO'),
        ('prefiero no decirlo','PREFIERO NO DECIRLO'),
    ]
    RH_OPCIONES = [
        ('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),
        ('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-'),
    ]

    tipo_doc         = models.CharField(max_length=20, choices=OPCIONES_TIPODOC)
    num_doc          = models.CharField(max_length=10, unique=True)
    email            = models.EmailField(unique=True, blank=False)
    genero           = models.CharField(max_length=20, choices=GENERO_OPCIONES)
    rh               = models.CharField(max_length=3,  choices=RH_OPCIONES)
    telefono         = PhoneNumberField(null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    tipo_poblacion   = models.CharField(max_length=50)
    ocupacion        = models.CharField(max_length=20)
    eps              = models.CharField(max_length=20)
    imagen           = models.ImageField(upload_to=ruta_directorio_usuario, blank=True, null=True)

    USERNAME_FIELD  = 'num_doc'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return f"{self.num_doc} - {self.get_full_name()}"

    def delete(self, *args, **kwargs):
        if self.imagen and self.imagen.name:
            self.eliminar_imagen()
        super().delete(*args, **kwargs)

    def eliminar_imagen(self):
        try:
            if self.imagen and self.imagen.name and os.path.isfile(self.imagen.path):
                os.remove(self.imagen.path)
                logger.info(f"Imagen eliminada: {self.imagen.path}")
            else:
                logger.warning(f"Imagen no encontrada: {self.imagen.path}")
        except Exception as e:
            logger.error(f"Error eliminando imagen: {e}")

    def clean(self):
        if self.fecha_nacimiento and self.fecha_nacimiento > timezone.now().date():
            raise ValidationError('La fecha de nacimiento no puede ser en el futuro.')
# endregion


# region Paciente
class Paciente(Usuario):
    OPCIONES_REGIMEN = [
        ('subsidiado',   'SUBSIDIADO'),
        ('contributivo', 'CONTRIBUTIVO'),
        ('otro',         'OTRO'),
    ]
    regimen = models.CharField(max_length=30, choices=OPCIONES_REGIMEN)

    def __str__(self):
        return f"{self.get_full_name()} - Paciente"
# endregion


# region Administrador
PERMISOS_POR_AREA = {
    'Odontologia': {
        'ver_pacientes':    True,
        'editar_pacientes': True,
        'ver_historia':     True,
        'gestion_usuarios': True,
        'ver_citas':        True,
        'gestionar_citas':  True,
    },
    'Cirugia': {
        'ver_pacientes':    True,
        'realizar_cirugia': True,
        'ver_historia':     True,
        'gestion_usuarios': True,
        'ver_citas':        True,
    },
    'General': {
        'ver_pacientes':    True,
        'ver_historia':     True,
        'gestion_usuarios': True,
        'ver_citas':        True,
        'gestionar_citas':  True,
    },
    'Rayos_x': {
        'ver_pacientes':     True,
        'ver_imagenes':      True,
        'realizar_imagenes': True,
        'gestion_usuarios':  True,
    },
}

class Administrador(Usuario):
    AREAS_MEDICAS = [
        ('Odontologia', 'Odontología'),
        ('Cirugia',     'Cirugía'),
        ('General',     'General'),
        ('Rayos_x',     'Rayos X'),
    ]
    rol_acceso            = models.CharField(max_length=100)
    centro_administracion = models.CharField(max_length=255, choices=AREAS_MEDICAS)
    permisos              = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.permisos:
            self.permisos = PERMISOS_POR_AREA.get(self.centro_administracion, {})
        super().save(*args, **kwargs)

    def tiene_permiso(self, permiso: str) -> bool:
        if not self.permisos:
            return False
        return self.permisos.get(permiso, False)

    def __str__(self):
        return f"{self.get_full_name()} - Administrador ({self.centro_administracion})"
# endregion


# region Medico
class Medico(Usuario):
    ESPECIALIDADES = [
        ('General',     'General'),
        ('Odontologia', 'Odontología'),
        ('Pediatria',   'Pediatría'),
    ]
    especialidad                = models.CharField(max_length=100, choices=ESPECIALIDADES)
    numero_registro_profesional = models.CharField(max_length=50)
    licencia_certificacion      = models.BooleanField(default=False)
    fecha_contratacion          = models.DateField()

    def __str__(self):
        return f"{self.get_full_name()} - Médico ({self.especialidad})"
# endregion


# region Consulta
class Consulta(models.Model):
    especialidad            = models.CharField(max_length=100, blank=True)
    tratamiento             = models.TextField(max_length=200)
    diagnostico_principal   = models.TextField(max_length=255)
    diagnostico_relacionado = models.TextField(max_length=255)
    motivo_consulta         = models.TextField(max_length=200)
    fecha_consulta          = models.DateField(auto_now_add=True)
    medico                  = models.ForeignKey(Medico,   on_delete=models.CASCADE, related_name='medico_consulta')
    paciente                = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')

    def __str__(self):
        return f"Consulta de {self.paciente} con {self.medico} el {self.fecha_consulta}"
# endregion


# region PerfilPaciente — corregido: ligado a Paciente, no a Consulta
class PerfilPaciente(models.Model):
    OPCIONES_VIDA_SEXUAL = [
        ('activo',    'ACTIVO'),
        ('no activo', 'NO ACTIVO'),
    ]
    # CORRECCIÓN: OneToOne con Paciente (antes apuntaba a Consulta)
    paciente              = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='perfil')
    tratamiento           = models.TextField(max_length=200, null=True, blank=True)
    vida_sexual           = models.CharField(max_length=50, choices=OPCIONES_VIDA_SEXUAL)
    ciclo_mestrual        = models.TextField(max_length=200, null=True, blank=True)
    sustancias_psicotivas = models.BooleanField(default=False)
    habitos_alimenticios  = models.TextField(max_length=200, null=True, blank=True)
    consumo_alcohol       = models.BooleanField(default=False)
    habito_sueño          = models.TextField(max_length=200, null=True, blank=True)
    antecedentes_personales = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.paciente}"
# endregion


# region Antecedente
class Antecedente(models.Model):
    descripcion      = models.TextField(max_length=200, null=True, blank=True)
    tipo_antecedente = models.TextField(max_length=200)
    paciente         = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='antecedentes')

    def __str__(self):
        return f"Antecedente de {self.paciente}: {self.tipo_antecedente}"
# endregion


# region Vacuna
class Vacuna(models.Model):
    nombre_vacuna    = models.CharField(max_length=150)
    fecha_aplicacion = models.DateField()
    dosis            = models.CharField(max_length=100)
    paciente         = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='vacunas')

    def __str__(self):
        return f"Vacuna {self.nombre_vacuna} para {self.paciente}"
# endregion


# region DatoQuirurgico
class DatoQuirurgico(models.Model):
    tipo_cirugia   = models.CharField(max_length=150)
    fecha_cirugia  = models.DateField()
    complicaciones = models.TextField(max_length=200)
    paciente       = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='datos_quirurgicos')
    medico         = models.ForeignKey(Medico,   on_delete=models.CASCADE, related_name='medico_datos_quirurgicos')

    def __str__(self):
        return f"Cirugía {self.tipo_cirugia} de {self.paciente}"
# endregion


# region HistoriaClinica
class HistoriaClinica(models.Model):
    ultima_atencion = models.DateField()
    tratamiento     = models.TextField()
    notas           = models.TextField()
    paciente        = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historia_clinica')

    def __str__(self):
        return f"Historia clínica de {self.paciente}"
# endregion


# region DatoAntropometrico
class DatoAntropometrico(models.Model):
    altura_decimal       = models.DecimalField(max_digits=5, decimal_places=2)
    peso                 = models.DecimalField(max_digits=5, decimal_places=2)
    indice_masa_corporal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    paciente             = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='datos_antropometricos')
    medico               = models.ForeignKey(Medico,   on_delete=models.CASCADE, related_name='medico_dato_antropometrico')

    def save(self, *args, **kwargs):
        # Calcula IMC automáticamente
        if self.peso and self.altura_decimal and self.altura_decimal > 0:
            self.indice_masa_corporal = round(
                float(self.peso) / (float(self.altura_decimal) ** 2), 2
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Datos antropométricos de {self.paciente}"
# endregion


# region HorarioMedico
class HorarioMedico(models.Model):
    OPCIONES_DIAS_SEMANA = [
        ('lunes',     'Lunes'),
        ('martes',    'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves',    'Jueves'),
        ('viernes',   'Viernes'),
        ('sabado',    'Sábado'),
        ('domingo',   'Domingo'),
    ]
    medico      = models.ForeignKey(Medico, on_delete=models.CASCADE)
    dia_semana  = models.CharField(max_length=10, choices=OPCIONES_DIAS_SEMANA, default='lunes')
    hora_inicio = models.TimeField()
    hora_fin    = models.TimeField()

    def __str__(self):
        return f"Horario de {self.medico} - {self.dia_semana}"
# endregion


# region AgendaMedica — DEPRECADA: usar Cita con filtros
# Se mantiene temporalmente para no romper migraciones existentes.
# No usar en código nuevo — consultar Cita filtrando por medico y fecha.
class AgendaMedica(models.Model):
    medico   = models.ForeignKey(Medico,   on_delete=models.CASCADE, related_name='medico_agenda')
    hora     = models.TimeField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='paciente_cita')
    motivo   = models.CharField(max_length=200)

    class Meta:
        verbose_name        = 'Agenda Médica (DEPRECADA)'
        verbose_name_plural = 'Agendas Médicas (DEPRECADAS)'

    def __str__(self):
        return f"Agenda de {self.medico} con {self.paciente} a las {self.hora}"
# endregion


# region Cita
class Cita(models.Model):
    OPCIONES_ESTADO_CITA = [
        ('DP',        'Disponible'),
        ('agendada',  'Agendada'),
        ('atendida',  'Atendida'),
        ('cancelada', 'Cancelada'),
        ('NA',        'No atendida'),
    ]
    fecha_cita     = models.DateField()
    hora_cita      = models.TimeField()
    estado_cita    = models.CharField(max_length=10, choices=OPCIONES_ESTADO_CITA, default='agendada')
    especialidad   = models.CharField(max_length=100, blank=True)
    medico         = models.ForeignKey(Medico,         on_delete=models.CASCADE, related_name='medico_citas')
    paciente       = models.ForeignKey(Paciente,       on_delete=models.CASCADE, related_name='paciente_agenda_cita')
    disponibilidad = models.ForeignKey('Disponibilidad', on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_asociadas')

    def __str__(self):
        return f"Cita de {self.paciente} con {self.medico} el {self.fecha_cita} a las {self.hora_cita}"
# endregion


# region CertificadoIncapacidad
class CertificadoIncapacidad(models.Model):
    medico                  = models.ForeignKey(Medico,   on_delete=models.CASCADE, related_name='medico_incapacidad_medica')
    paciente                = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='paciente_incapacidad_medica')
    dias_incapacidad        = models.IntegerField()  # CORRECCIÓN: era CharField
    motivo_incapacidad      = models.CharField(max_length=255)
    fecha_inicio            = models.DateField(default=timezone.now)
    fecha_fin               = models.DateField(null=True, blank=True)
    diagnostico_principal   = models.TextField(max_length=255)
    diagnostico_relacionado = models.TextField(max_length=255)
    observaciones           = models.CharField(max_length=255)

    def __str__(self):
        return f"Incapacidad de {self.paciente} por {self.dias_incapacidad} días"
# endregion


# region RecetaMedica
class RecetaMedica(models.Model):
    medico                  = models.ForeignKey(Medico,   on_delete=models.CASCADE, related_name='medico_receta_medica')
    paciente                = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='paciente_receta_medica')
    medicamento             = models.CharField(max_length=100)
    concentracion           = models.CharField(max_length=100)
    duracion                = models.CharField(max_length=100)
    cantidad                = models.CharField(max_length=100)
    via_administracion      = models.CharField(max_length=20)
    intervalo               = models.CharField(max_length=100, null=True, blank=True)
    recomendaciones         = models.CharField(max_length=255, null=True, blank=True)
    indicaciones            = models.TextField(null=True, blank=True)
    fecha_medicado          = models.DateField(null=True, blank=True)
    diagnostico_principal   = models.ForeignKey('TablaReferenciaCIE10', on_delete=models.CASCADE,  related_name='receta_diagnostico_principal')
    diagnostico_relacionado = models.ForeignKey('TablaReferenciaCIE10', on_delete=models.SET_NULL, related_name='receta_diagnostico_relacionado', null=True, blank=True)

    def __str__(self):
        return f"Receta para {self.paciente}: {self.medicamento}"
# endregion


# region OrdenMedica
class OrdenMedica(models.Model):
    ESTADO_ORDEN = [
        ('VIG', 'Vigente'),
        ('VEN', 'Vencida'),
        ('AG',  'Agendada'),
        ('PA',  'Por autorizar'),
        ('AUT', 'Autorizada'),
    ]
    cups                    = models.CharField(max_length=10)  # CORRECCIÓN: eliminado unique=True
    medico                  = models.ForeignKey(Medico,   on_delete=models.CASCADE, related_name='medico_orden_medica')
    paciente                = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='paciente_orden_medica')
    especialidad_referido   = models.CharField(max_length=255)
    cantidad                = models.CharField(max_length=4)
    diagnostico_principal   = models.TextField(max_length=255)
    diagnostico_relacionado = models.TextField(max_length=255)
    motivo                  = models.CharField(max_length=255)
    fecha_ordenado          = models.DateField(default=timezone.now)
    vigencia                = models.DateField()
    estado                  = models.CharField(max_length=15, choices=ESTADO_ORDEN)

    def __str__(self):
        return f"Orden CUPS {self.cups} para {self.paciente} - {self.estado}"

    class Meta:
        ordering = ['-fecha_ordenado']
# endregion


# region Disponibilidad
class Disponibilidad(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('ocupado',    'Ocupado'),
        ('cancelado',  'Cancelado'),
        ('pendiente',  'Pendiente'),
    ]
    TIPO_CITA = [
        ('General',     'General'),
        ('Odontologia', 'Odontología'),
        ('Pediatria',   'Pediatría'),
    ]
    medico        = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha         = models.DateField()
    hora_inicio   = models.TimeField()
    hora_fin      = models.TimeField()
    tipo_cita     = models.CharField(max_length=50, choices=TIPO_CITA)
    estado        = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    max_pacientes = models.PositiveIntegerField(default=1)
    duracion      = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.medico} - {self.fecha} de {self.hora_inicio} a {self.hora_fin}"

    class Meta:
        ordering = ['-fecha', 'hora_inicio']
# endregion


# region TablaReferenciaCIE10
class TablaReferenciaCIE10(models.Model):
    tabla                     = models.CharField(max_length=5)
    codigo                    = models.CharField(max_length=5, unique=True)
    nombre                    = models.CharField(max_length=250)
    descripcion               = models.CharField(max_length=250)
    habilitado                = models.CharField(max_length=2)
    extra_i_aplica_a_sexo     = models.CharField(max_length=10)
    extra_ii_edad_minima      = models.CharField(max_length=3)
    extra_iii_edad_maxima     = models.CharField(max_length=3)
    extra_iv_grupo_mortalidad = models.CharField(max_length=10)
    extra_v                   = models.CharField(max_length=255)
    extra_vi_capitulo         = models.CharField(max_length=3)
    extra_x                   = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
# endregion