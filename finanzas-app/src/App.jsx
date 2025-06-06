import { useState } from 'react'
import './App.css'
import AppRoutes from './routing/AppRoutes'
import Login from './components/pages/Login'
import Typography from '@mui/material/Typography'
import { Container } from '@mui/material'

function App() {
  const [token, setToken] = useState(0)

  if (!token) {
    return <Login onLogin={setToken} />
  }

  return (
    <AppRoutes token = {token}/>
  )
}

export default App
