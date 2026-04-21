import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { useAuth } from './context/AuthContext'

import Home from './pages/Home'
import Login from './pages/Login'
import PerfilMedico from './pages/Medico/PerfilMedico'
import PerfilPaciente from './pages/Paciente/PerfilPaciente'
import PerfilAdministrador from './pages/Administrador/PerfilAdministrador'

const PrivateRoute = ({ children }) => {
  const { isAuthenticated } = useAuth()
  return isAuthenticated ? children : <Navigate to="/login" />
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/medico" element={<PrivateRoute><PerfilMedico /></PrivateRoute>} />
          <Route path="/paciente" element={<PrivateRoute><PerfilPaciente /></PrivateRoute>} />
          <Route path="/administrador" element={<PrivateRoute><PerfilAdministrador /></PrivateRoute>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App