import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import '../assets/css/Login.css'

const LogoIcon = () => (
  <svg width="40" height="40" viewBox="0 0 100 100" fill="none">
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

const Login = () => {
  const [tipoDoc,  setTipoDoc]  = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error,    setError]    = useState('')
  const { login, loading }      = useAuth()
  const navigate                = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      // Ahora enviamos los 3 campos al backend
      const data = await login(tipoDoc, username, password)
      if (data.tipo_usuario === 'medico')             navigate('/medico')
      else if (data.tipo_usuario === 'paciente')      navigate('/paciente')
      else if (data.tipo_usuario === 'administrador') navigate('/administrador')
      else navigate('/')
    } catch (err) {
      // Muestra el mensaje de error del backend si existe
      const msg = err?.response?.data?.non_field_errors?.[0]
        || err?.response?.data?.detail
        || 'Credenciales incorrectas. Intenta de nuevo.'
      setError(msg)
    }
  }

  return (
    <div className="loginPage">

      {/* ─── Lado izquierdo ─── */}
      <div className="loginLeft">
        <div className="loginLeftDecor" />
        <div className="loginLeftDecor2" />
        <div className="loginLeftLogo">
          <LogoIcon />
          <span className="loginLeftLogoText">IZEL</span>
        </div>
        <h2 className="loginLeftTitle">
          Bienvenido al sistema<br />
          <span>de gestión hospitalaria</span>
        </h2>
        <p className="loginLeftDesc">
          Accede a tu historia clínica, agenda citas médicas y gestiona
          tu salud desde cualquier lugar, de forma segura y sencilla.
        </p>
      </div>

      {/* ─── Lado derecho ─── */}
      <div className="loginRight">
        <div className="loginCard">
          <h1 className="loginCardTitle">Iniciar sesión</h1>
          <p className="loginCardSub">Completa los siguientes campos</p>

          <form onSubmit={handleSubmit} className="loginForm">

            {/* Tipo de documento */}
            <div className="floatGroup">
              <select
                className={`loginInput loginSelect ${tipoDoc ? 'hasValue' : ''}`}
                value={tipoDoc}
                onChange={(e) => { setTipoDoc(e.target.value); setUsername('') }}
                required
              >
                <option value="" disabled hidden></option>
                <option value="CC">Cédula de Ciudadanía</option>
                <option value="CE">Cédula de Extranjería</option>
                <option value="NIT">NIT</option>
                <option value="PPT">Permiso de Protección Temporal</option>
              </select>
              <label className={`floatLabel ${tipoDoc ? 'active' : ''}`}>
                Tipo de documento
              </label>
            </div>

            {/* Número de documento — bloqueado hasta seleccionar tipo */}
            <div className="floatGroup">
              <input
                type="text"
                className={`loginInput ${!tipoDoc ? 'disabled' : ''}`}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={!tipoDoc}
                required
                placeholder=" "
              />
              <label className={`floatLabel ${username ? 'active' : ''}`}>
                {tipoDoc ? 'Número de documento' : 'Selecciona primero el tipo'}
              </label>
            </div>

            {/* Contraseña */}
            <div className="floatGroup">
              <input
                type="password"
                className="loginInput"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder=" "
              />
              <label className={`floatLabel ${password ? 'active' : ''}`}>
                Contraseña
              </label>
            </div>

            {error && <p className="loginError">{error}</p>}

            <button
              type="submit"
              className={loading || !tipoDoc ? 'loginBtnDisabled' : 'loginBtn'}
              disabled={loading || !tipoDoc}
            >
              {loading ? 'Ingresando...' : 'Iniciar sesión'}
            </button>
          </form>

          <div className="loginRecuperar">
            <a href="#">¿Olvidaste tu contraseña?</a>
          </div>
          <div className="loginVolver">
            <Link to="/">← Volver al inicio</Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login