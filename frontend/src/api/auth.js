import api from './axios'

// ─── Login ────────────────────────────────────────────────────────────────────
export const login = async (tipo_doc, username, password) => {
  const response = await api.post('/auth/login/', { tipo_doc, username, password })
  const { access, refresh, tipo_usuario, especialidad, area, usuario } = response.data

  localStorage.setItem('access_token',  access)
  localStorage.setItem('refresh_token', refresh)
  localStorage.setItem('tipo_usuario',  tipo_usuario)
  localStorage.setItem('especialidad',  especialidad || '')
  localStorage.setItem('area',          area || '')
  localStorage.setItem('usuario',       JSON.stringify(usuario))

  return response.data
}

// ─── Logout ───────────────────────────────────────────────────────────────────
export const logout = async () => {
  try {
    const refresh = localStorage.getItem('refresh_token')
    await api.post('/auth/logout/', { refresh })
  } finally {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('tipo_usuario')
    localStorage.removeItem('especialidad')
    localStorage.removeItem('area')
    localStorage.removeItem('usuario')
  }
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
export const getMe           = async () => (await api.get('/auth/me/')).data
export const isAuthenticated = ()        => !!localStorage.getItem('access_token')
export const getTipoUsuario  = ()        => localStorage.getItem('tipo_usuario')
export const getEspecialidad = ()        => localStorage.getItem('especialidad')
export const getArea         = ()        => localStorage.getItem('area')