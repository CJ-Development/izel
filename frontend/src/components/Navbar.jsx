import { Link, useNavigate, useLocation } from 'react-router-dom'
import '../assets/css/Navbar.css'

const LogoIcon = () => (
  <svg width="36" height="36" viewBox="0 0 100 100" fill="none">
    <circle cx="50" cy="42" r="26" stroke="#A3BAC3" strokeWidth="4"/>
    <rect x="43" y="26" width="14" height="32" rx="3" fill="#A3BAC3"/>
    <rect x="34" y="35" width="32" height="14" rx="3" fill="#A3BAC3"/>
    <line x1="10" y1="42" x2="24" y2="42" stroke="#A3BAC3" strokeWidth="3" strokeLinecap="round"/>
    <line x1="10" y1="42" x2="10" y2="34" stroke="#A3BAC3" strokeWidth="3" strokeLinecap="round"/>
    <circle cx="10" cy="34" r="3" fill="#A3BAC3"/>
    <line x1="76" y1="42" x2="90" y2="42" stroke="#A3BAC3" strokeWidth="3" strokeLinecap="round"/>
    <line x1="90" y1="42" x2="90" y2="52" stroke="#A3BAC3" strokeWidth="3" strokeLinecap="round"/>
    <circle cx="90" cy="52" r="3" fill="#A3BAC3"/>
  </svg>
)

// Mapeo de roles a rutas de dashboard
const ROLE_DASHBOARD = {
  admin:     '/admin/dashboard',
  medico:    '/medico/dashboard',
  paciente:  '/paciente/dashboard',
  enfermera: '/enfermera/dashboard',
}

// Mapeo de roles a etiquetas legibles
const ROLE_LABEL = {
  admin:     'Administrador',
  medico:    'Médico',
  paciente:  'Paciente',
  enfermera: 'Enfermera',
}

const Navbar = () => {
  const navigate  = useNavigate()
  const location  = useLocation()

  // Lee el usuario guardado en sessionStorage/localStorage (ajusta según tu auth)
  const rawUser  = sessionStorage.getItem('user') || localStorage.getItem('user')
  const user     = rawUser ? JSON.parse(rawUser) : null
  const role     = user?.rol || user?.role || null   // ← ajusta el key según tu backend

  const isHome   = location.pathname === '/'

  /* ── Scroll suave: si ya estamos en Home desplazamos,
        si no, navegamos primero y luego esperamos el mount ── */
  const scrollTo = (sectionId) => {
    if (isHome) {
      document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' })
    } else {
      navigate('/')
      // Pequeño delay para que React monte la página antes de buscar el elemento
      setTimeout(() => {
        document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' })
      }, 120)
    }
  }

  const handleLogout = () => {
    sessionStorage.removeItem('user')
    localStorage.removeItem('user')
    navigate('/')
  }

  return (
    <nav className="nav">
      <Link to="/" className="navLogo">
        <LogoIcon />
        <span className="navLogoText">IZEL</span>
      </Link>

      <div className="navLinks">
       <button className="navAnchor" onClick={() => scrollTo('inicio')}>
          Inicio
        </button>


        <button className="navAnchor" onClick={() => scrollTo('nosotros')}>
          Sobre nosotros
        </button>

        <button className="navAnchor" onClick={() => scrollTo('servicios')}>
          Servicios
        </button>

        {user ? (
          /* ── Usuario autenticado ── */
          <div className="navUser">
            <span className="navUserBadge">
              {ROLE_LABEL[role] ?? role}
            </span>
            <span className="navUserName">{user.nombre || user.name}</span>
            <button
              className="btnDashboard"
              onClick={() => navigate(ROLE_DASHBOARD[role] ?? '/')}
            >
              Mi panel
            </button>
            <button className="btnLogout" onClick={handleLogout}>
              Salir
            </button>
          </div>
        ) : (
          /* ── Sin sesión ── */
          <button className="btnLogin" onClick={() => navigate('/login')}>
            Ingresar
          </button>
        )}
      </div>
    </nav>
  )
}

export default Navbar