import '../../assets/css/PerfilMedico.css'; 
// --- Datos de ejemplo (luego los traes del backend) ---
const estadisticas = [
  { label: 'Citas de hoy',       valor: 8, sub: '3 pendientes',     tipo: 'normal' },
  { label: 'Atendidos',          valor: 5, sub: 'de 8 programados', tipo: 'muted'  },
  { label: 'Cancelaciones',      valor: 1, sub: 'Hoy',              tipo: 'warn'   },
  { label: 'Órdenes pendientes', valor: 4, sub: 'Requieren firma',  tipo: 'warn'   },
];
 
const citas = [
  { hora: '08:00', nombre: 'María Pérez',    tipo: 'Control hipertensión', estado: 'atendido',  iniciales: 'MP' },
  { hora: '09:30', nombre: 'Carlos García',  tipo: 'Consulta general',     estado: 'atendido',  iniciales: 'CG' },
  { hora: '11:00', nombre: 'Lucía Torres',   tipo: 'Resultado exámenes',   estado: 'en-curso',  iniciales: 'LT' },
  { hora: '14:00', nombre: 'Roberto Vargas', tipo: 'Primera consulta',     estado: 'pendiente', iniciales: 'RV' },
  { hora: '15:30', nombre: 'Ana Molina',     tipo: 'Seguimiento',          estado: 'pendiente', iniciales: 'AM' },
];
 
const alertas = [
  { tipo: 'rojo',     texto: 'Resultado crítico: glucosa alta — Carlos García', tiempo: 'Hace 15 min'  },
  { tipo: 'amarillo', texto: '4 órdenes médicas esperan tu firma',              tiempo: 'Hace 1 hora'  },
  { tipo: 'azul',     texto: 'Mensaje de enfermería — Cama 3',                  tiempo: 'Hace 2 horas' },
];
 
const accesos = [
  { icon: '📋', label: 'Historia clínica' },
  { icon: '💊', label: 'Nueva orden'      },
  { icon: '🔬', label: 'Solicitar examen' },
  { icon: '📝', label: 'Incapacidades'    },
];
 
const etiquetaEstado = {
  atendido:   'Atendido',
  'en-curso': 'En curso',
  pendiente:  'Pendiente',
};
 
// --- Sub-componentes ---
const StatCard = ({ label, valor, sub, tipo }) => (
  <div className="stat-card">
    <p className="stat-label">{label}</p>
    <p className="stat-valor">{valor}</p>
    <p className={`stat-sub sub-${tipo}`}>{sub}</p>
  </div>
);
 
const CitaRow = ({ hora, nombre, tipo, estado, iniciales }) => (
  <div className="cita-row">
    <span className="hora">{hora}</span>
    <div className="avatar">{iniciales}</div>
    <div className="cita-info">
      <p className="cita-nombre">{nombre}</p>
      <p className="cita-tipo">{tipo}</p>
    </div>
    <span className={`estado estado-${estado}`}>
      {etiquetaEstado[estado]}
    </span>
  </div>
);
 
const AlertaItem = ({ tipo, texto, tiempo }) => (
  <div className="alerta-row">
    <div className={`dot dot-${tipo}`} />
    <div>
      <p className="alerta-texto">{texto}</p>
      <p className="alerta-tiempo">{tiempo}</p>
    </div>
  </div>
);
 
// --- Componente principal ---
const PerfilMedico = () => {
  const hoy = new Date().toLocaleDateString('es-CO', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });
 
  return (
    <div className="dash">
 
      {/* Encabezado */}
      <div className="pm-header">
        <div>
          <h1 className="pm-titulo">¡Buenos días, Dr. Ramírez!</h1>
          <p className="pm-subtitulo">{hoy} · Turno: 8:00 am – 4:00 pm</p>
        </div>
        <button className="notif-btn">
          Notificaciones <span className="badge">{alertas.length}</span>
        </button>
        <button>
            Cerrar Sesion 
        </button>
      </div>
 
      {/* Estadísticas */}
      <div className="stats-grid">
        {estadisticas.map((e) => (
          <StatCard key={e.label} {...e} />
        ))}
      </div>
 
      {/* Contenido principal */}
      <div className="main-grid">
 
        {/* Agenda */}
        <div className="panel">
          <div className="panel-header">
            <span className="panel-titulo">Agenda del día</span>
            <button className="ver-todo">Ver agenda completa →</button>
          </div>
          {citas.map((c) => (
            <CitaRow key={c.nombre} {...c} />
          ))}
        </div>
 
        {/* Columna derecha */}
        <div className="right-col">
 
          {/* Alertas */}
          <div className="panel">
            <div className="panel-header">
              <span className="panel-titulo">Alertas</span>
            </div>
            {alertas.map((a, i) => (
              <AlertaItem key={i} {...a} />
            ))}
          </div>
 
          {/* Accesos rápidos */}
          <div className="panel">
            <div className="panel-header">
              <span className="panel-titulo">Accesos rápidos</span>
            </div>
            <div className="accesos-grid">
              {accesos.map((a) => (
                <button key={a.label} className="acceso-btn">
                  <span className="acceso-icon">{a.icon}</span>
                  <span className="acceso-label">{a.label}</span>
                </button>
              ))}
            </div>
          </div>
 
        </div>
      </div>
    </div>
  );
};
 
export default PerfilMedico;