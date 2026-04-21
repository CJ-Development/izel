from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import api_views

urlpatterns = [

    # ─── Autenticación ────────────────────────────────────────────────────────
    path('auth/login/',   api_views.LoginView.as_view(),   name='api_login'),
    path('auth/logout/',  api_views.LogoutView.as_view(),  name='api_logout'),
    path('auth/refresh/', TokenRefreshView.as_view(),      name='api_token_refresh'),
    path('auth/me/',      api_views.MeView.as_view(),      name='api_me'),

    # ─── Pacientes ────────────────────────────────────────────────────────────
    path('pacientes/',           api_views.PacienteListView.as_view(),   name='api_pacientes'),
    path('pacientes/<int:pk>/',  api_views.PacienteDetailView.as_view(), name='api_paciente_detail'),

    # ─── Médicos ──────────────────────────────────────────────────────────────
    path('medicos/',             api_views.MedicoListView.as_view(),     name='api_medicos'),
    path('medicos/<int:pk>/',    api_views.MedicoDetailView.as_view(),   name='api_medico_detail'),

    # ─── Disponibilidad ───────────────────────────────────────────────────────
    path('disponibilidad/',          api_views.DisponibilidadListView.as_view(),   name='api_disponibilidad'),
    path('disponibilidad/<int:pk>/', api_views.DisponibilidadDetailView.as_view(), name='api_disponibilidad_detail'),

    # ─── Citas ────────────────────────────────────────────────────────────────
    path('citas/',          api_views.CitaListView.as_view(),   name='api_citas'),
    path('citas/<int:pk>/', api_views.CitaDetailView.as_view(), name='api_cita_detail'),

    # ─── Consultas ────────────────────────────────────────────────────────────
    path('consultas/',          api_views.ConsultaListView.as_view(),   name='api_consultas'),
    path('consultas/<int:pk>/', api_views.ConsultaDetailView.as_view(), name='api_consulta_detail'),

    # ─── Recetas ──────────────────────────────────────────────────────────────
    path('recetas/',          api_views.RecetaListView.as_view(),   name='api_recetas'),
    path('recetas/<int:pk>/', api_views.RecetaDetailView.as_view(), name='api_receta_detail'),

    # ─── Órdenes médicas ──────────────────────────────────────────────────────
    path('ordenes/',          api_views.OrdenListView.as_view(),   name='api_ordenes'),
    path('ordenes/<int:pk>/', api_views.OrdenDetailView.as_view(), name='api_orden_detail'),

    # ─── Certificados de incapacidad ──────────────────────────────────────────
    path('incapacidades/',          api_views.IncapacidadListView.as_view(),   name='api_incapacidades'),
    path('incapacidades/<int:pk>/', api_views.IncapacidadDetailView.as_view(), name='api_incapacidad_detail'),

    # ─── CIE10 ────────────────────────────────────────────────────────────────
    path('cie10/', api_views.CIE10ListView.as_view(), name='api_cie10'),
]
