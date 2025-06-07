import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { BrowserRouter } from 'react-router-dom'
import AppRoutes from './routing/AppRoutes'
import { CssBaseline, ThemeProvider } from '@mui/material'
import AppTheme from './theme/AppTheme.jsx'
import ReactDOM from 'react-dom/client'
import React from 'react';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  </React.StrictMode>
);
