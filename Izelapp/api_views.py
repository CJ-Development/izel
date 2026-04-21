from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q

from .models import (
    Paciente, Medico, Administrador,
    Consulta, Cita, Disponibilidad,
    RecetaMedica, OrdenMedica, CertificadoIncapacidad,
    TablaReferenciaCIE10
)
from .serializers import (
    LoginSerializer, PacienteSerializer, MedicoSerializer,
    MedicoResumenSerializer, AdministradorSerializer,
    DisponibilidadSerializer, CitaSerializer, ConsultaSerializer,
    RecetaMedicaSerializer, OrdenMedicaSerializer,
    CertificadoIncapacidadSerializer, CIE10Serializer
)


# ─── Autenticación ────────────────────────────────────────────────────────────

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.validated_data['usuario']

        refresh = RefreshToken.for_user(usuario)

        # Determina el tipo de usuario
        tipo = None
        if hasattr(usuario, 'paciente'):
            tipo = 'paciente'
        elif hasattr(usuario, 'medico'):
            tipo = 'medico'
        elif hasattr(usuario, 'administrador'):
            tipo = 'administrador'

        return Response({
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
            'tipo_usuario': tipo,
            'usuario': {
                'id':         usuario.id,
                'nombre':     usuario.first_name,
                'apellido':   usuario.last_name,
                'email':      usuario.email,
                'num_doc':    usuario.num_doc,
            }
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Sesión cerrada correctamente.'})
        except Exception:
            return Response({'detail': 'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    """Retorna la info del usuario autenticado"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        tipo = None
        data = {}

        if hasattr(usuario, 'paciente'):
            tipo = 'paciente'
            data = PacienteSerializer(usuario.paciente).data
        elif hasattr(usuario, 'medico'):
            tipo = 'medico'
            data = MedicoSerializer(usuario.medico).data
        elif hasattr(usuario, 'administrador'):
            tipo = 'administrador'
            data = AdministradorSerializer(usuario.administrador).data

        return Response({'tipo_usuario': tipo, 'perfil': data})


# ─── Pacientes ────────────────────────────────────────────────────────────────

class PacienteListView(generics.ListCreateAPIView):
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Paciente.objects.all()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(num_doc__icontains=search)
            )
        return queryset


class PacienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]


# ─── Médicos ──────────────────────────────────────────────────────────────────

class MedicoListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Medico.objects.all()
        especialidad = self.request.query_params.get('especialidad')
        if especialidad:
            queryset = queryset.filter(especialidad=especialidad)
        return queryset

    def get_serializer_class(self):
        if self.request.query_params.get('resumen'):
            return MedicoResumenSerializer
        return MedicoSerializer


class MedicoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    permission_classes = [IsAuthenticated]


# ─── Disponibilidad ───────────────────────────────────────────────────────────

class DisponibilidadListView(generics.ListCreateAPIView):
    serializer_class = DisponibilidadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Disponibilidad.objects.filter(estado='disponible')
        medico = self.request.query_params.get('medico')
        fecha  = self.request.query_params.get('fecha')
        tipo   = self.request.query_params.get('tipo_cita')
        if medico:
            queryset = queryset.filter(medico_id=medico)
        if fecha:
            queryset = queryset.filter(fecha=fecha)
        if tipo:
            queryset = queryset.filter(tipo_cita=tipo)
        return queryset


class DisponibilidadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Disponibilidad.objects.all()
    serializer_class = DisponibilidadSerializer
    permission_classes = [IsAuthenticated]


# ─── Citas ────────────────────────────────────────────────────────────────────

class CitaListView(generics.ListCreateAPIView):
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        if hasattr(usuario, 'paciente'):
            return Cita.objects.filter(paciente=usuario.paciente)
        elif hasattr(usuario, 'medico'):
            return Cita.objects.filter(medico=usuario.medico)
        return Cita.objects.all()


class CitaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]


# ─── Consultas ────────────────────────────────────────────────────────────────

class ConsultaListView(generics.ListCreateAPIView):
    serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        if hasattr(usuario, 'paciente'):
            return Consulta.objects.filter(paciente=usuario.paciente)
        elif hasattr(usuario, 'medico'):
            return Consulta.objects.filter(medico=usuario.medico)
        return Consulta.objects.all()


class ConsultaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]


# ─── Recetas ──────────────────────────────────────────────────────────────────

class RecetaListView(generics.ListCreateAPIView):
    serializer_class = RecetaMedicaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        if hasattr(usuario, 'paciente'):
            return RecetaMedica.objects.filter(paciente=usuario.paciente)
        elif hasattr(usuario, 'medico'):
            return RecetaMedica.objects.filter(medico=usuario.medico)
        return RecetaMedica.objects.all()


class RecetaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecetaMedica.objects.all()
    serializer_class = RecetaMedicaSerializer
    permission_classes = [IsAuthenticated]


# ─── Órdenes médicas ──────────────────────────────────────────────────────────

class OrdenListView(generics.ListCreateAPIView):
    serializer_class = OrdenMedicaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        if hasattr(usuario, 'paciente'):
            return OrdenMedica.objects.filter(paciente=usuario.paciente)
        elif hasattr(usuario, 'medico'):
            return OrdenMedica.objects.filter(medico=usuario.medico)
        return OrdenMedica.objects.all()


class OrdenDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrdenMedica.objects.all()
    serializer_class = OrdenMedicaSerializer
    permission_classes = [IsAuthenticated]


# ─── Certificados de incapacidad ──────────────────────────────────────────────

class IncapacidadListView(generics.ListCreateAPIView):
    serializer_class = CertificadoIncapacidadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        if hasattr(usuario, 'paciente'):
            return CertificadoIncapacidad.objects.filter(paciente=usuario.paciente)
        elif hasattr(usuario, 'medico'):
            return CertificadoIncapacidad.objects.filter(medico=usuario.medico)
        return CertificadoIncapacidad.objects.all()


class IncapacidadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CertificadoIncapacidad.objects.all()
    serializer_class = CertificadoIncapacidadSerializer
    permission_classes = [IsAuthenticated]


# ─── CIE10 ────────────────────────────────────────────────────────────────────

class CIE10ListView(generics.ListAPIView):
    serializer_class = CIE10Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TablaReferenciaCIE10.objects.all()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) |
                Q(nombre__icontains=search)
            )
        return queryset[:50]  # Máximo 50 resultados para no sobrecargar
