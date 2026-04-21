import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import '../assets/css/Home.css'

const servicios = [
  {
    titulo: 'Consulta General',
    desc: 'Atención médica general para diagnóstico, seguimiento y tratamiento de enfermedades comunes.',
    icono: (
      <svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14" strokeLinecap="round"/></svg>
    )
  },
  {
    titulo: 'Especialistas',
    desc: 'Odontología, cirugía, rayos X y más. Médicos especializados para cada necesidad.',
    icono: (
      <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M6 20v-2a6 6 0 0112 0v2" strokeLinecap="round"/></svg>
    )
  },
  {
    titulo: 'Urgencias 24/7',
    desc: 'Servicio de urgencias disponible las 24 horas, los 7 días de la semana para tu tranquilidad.',
    icono: (
      <svg viewBox="0 0 24 24"><path d="M12 2l3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1z" strokeLinecap="round" strokeLinejoin="round"/></svg>
    )
  },
  {
    titulo: 'Vacunación',
    desc: 'Programa de vacunación para niños y adultos según el esquema nacional de inmunización.',
    icono: (
      <svg viewBox="0 0 24 24"><path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round"/><circle cx="12" cy="12" r="9"/></svg>
    )
  },
  {
    titulo: 'Laboratorio Clínico',
    desc: 'Análisis clínicos y de laboratorio con resultados precisos y entrega oportuna.',
    icono: (
      <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 12h8M12 8v8" strokeLinecap="round"/></svg>
    )
  },
  {
    titulo: 'Agendamiento en línea',
    desc: 'Agenda tu cita desde cualquier lugar, elige tu médico y horario de forma fácil y rápida.',
    icono: (
      <svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18" strokeLinecap="round"/></svg>
    )
  },
]

const Home = () => {
  const navigate = useNavigate()

  return (
    <>
      <Navbar />

      {/* Hero */}
      <section id='inicio' className="hero">
        <div className="heroText">
          <div className="heroBadge">EPS Izel — Soacha, Cundinamarca</div>
          <h1 className="heroTitle">
            Tu salud en manos<br />
            <span>de los mejores</span>
          </h1>
          <p className="heroDesc">
            Somos un hospital comprometido con la salud de nuestra comunidad.
            Ofrecemos atención médica integral con calidad, empatía y tecnología.
          </p>
          <div className="heroBtns">
            <button className="btnPrimary" onClick={() => navigate('/login')}>
              Agendar cita
            </button>
            <button className="btnOutline" onClick={() => navigate('/sobre-nosotros')}>
              Conocer más
            </button>
          </div>
        </div>

        <div className="heroStats">
          <div className="statCard">
            <div className="statNum">+2.400</div>
            <div className="statLabel">Pacientes atendidos</div>
            <div className="statBar"><div className="statBarFill" style={{ width: '85%' }} /></div>
          </div>
          <div className="statCard">
            <div className="statNum">12</div>
            <div className="statLabel">Médicos disponibles hoy</div>
            <div className="statBar"><div className="statBarFill" style={{ width: '60%' }} /></div>
          </div>
          <div className="statCard">
            <div className="statNum">4</div>
            <div className="statLabel">Especialidades médicas</div>
            <div className="statBar"><div className="statBarFill" style={{ width: '40%' }} /></div>
          </div>
        </div>
      </section>

      {/* Sobre nosotros */}
      <section id='nosotros' className="nosotros">
        <div className="nosotrosImgWrap">
          <div className="nosotrosLogoBig">
            <svg width="90" height="90" viewBox="0 0 100 100" fill="none">
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
          </div>
        </div>
        <div  className="nosotrosContent">
          <div className="sectionTag">Sobre nosotros</div>
          <h2 className="sectionTitle">Comprometidos con tu bienestar desde el primer día</h2>
          <p className="sectionDesc">
            En EPS Izel trabajamos para brindar atención médica de calidad a toda nuestra comunidad
            en Soacha. Contamos con profesionales capacitados, tecnología moderna y un enfoque
            humano en cada consulta.
          </p>
          <div className="valores">
            <div className="valor">Calidad</div>
            <div className="valor">Empatía</div>
            <div className="valor">Tecnología</div>
            <div className="valor">Compromiso</div>
          </div>
        </div>
      </section>

      {/* Servicios */}
      <section id='servicios' className="servicios">
        <div className="serviciosSectionTag">Servicios</div>
        <h2 className="serviciosSectionTitle">Lo que ofrecemos</h2>
        <p className="serviciosSub">Atención integral para cada etapa de tu salud</p>
        <div className="cardsGrid">
          {servicios.map((s, i) => (
            <div key={i} className="svcCard">
              <div className="svcIcon">{s.icono}</div>
              <div className="svcTitle">{s.titulo}</div>
              <div className="svcDesc">{s.desc}</div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="cta">
        <h2 className="ctaTitle">¿Listo para cuidar tu salud?</h2>
        <p className="ctaSub">Agenda tu cita hoy o ingresa al sistema con tu cuenta</p>
        <div className="ctaBtns">
          <button className="btnPrimary" onClick={() => navigate('/login')}>Agendar cita</button>
          <button className="btnOutline" onClick={() => navigate('/login')}>Iniciar sesión</button>
        </div>
      </section>

      <Footer />
    </>
  )
}

export default Home
