import { useState } from 'react'
import './App.css'
import AppRoutes from './routing/AppRoutes'

import Typography from '@mui/material/Typography'
import { Container } from '@mui/material'

function App() {
  const [count, setCount] = useState(0)

  return (
    <AppRoutes />
  )
}

export default App
