import { createContext, useContext, useState } from 'react'
import { login as loginApi, logout as logoutApi, isAuthenticated, getTipoUsuario, getEspecialidad, getArea } from '../api/auth'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [usuario, setUsuario] = useState(() => {
    const stored = localStorage.getItem('usuario')
    return stored ? JSON.parse(stored) : null
  })
  const [tipoUsuario,  setTipoUsuario]  = useState(() => getTipoUsuario())
  const [especialidad, setEspecialidad] = useState(() => getEspecialidad())
  const [area,         setArea]         = useState(() => getArea())
  const [loading,      setLoading]      = useState(false)

  const login = async (tipo_doc, username, password) => {
    setLoading(true)
    try {
      const data = await loginApi(tipo_doc, username, password)
      setUsuario(data.usuario)
      setTipoUsuario(data.tipo_usuario)
      setEspecialidad(data.especialidad || '')
      setArea(data.area || '')
      return data
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    await logoutApi()
    setUsuario(null)
    setTipoUsuario(null)
    setEspecialidad(null)
    setArea(null)
  }

  return (
    <AuthContext.Provider value={{
      usuario,
      tipoUsuario,
      especialidad,
      area,
      loading,
      login,
      logout,
      isAuthenticated: isAuthenticated(),
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth debe usarse dentro de AuthProvider')
  return context
}