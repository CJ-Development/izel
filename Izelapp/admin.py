from django.contrib import admin
from .models import (
    Usuario, Paciente, Medico, Administrador,
    Consulta, Cita, Disponibilidad,
    RecetaMedica, OrdenMedica, CertificadoIncapacidad,
    PerfilPaciente, TablaReferenciaCIE10,
    HorarioMedico, AgendaMedica
)

admin.site.register(Usuario)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Administrador)
admin.site.register(Consulta)
admin.site.register(Cita)
admin.site.register(Disponibilidad)
admin.site.register(RecetaMedica)
admin.site.register(OrdenMedica)
admin.site.register(CertificadoIncapacidad)
admin.site.register(PerfilPaciente)
admin.site.register(TablaReferenciaCIE10)
admin.site.register(HorarioMedico)
admin.site.register(AgendaMedica)