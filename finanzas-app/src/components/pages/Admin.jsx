import React, { useEffect, useState } from 'react';
// 1. Importar Link de react-router-dom
import { Link as RouterLink } from 'react-router-dom';
import {
  AppBar,
  Box,
  CssBaseline,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Toolbar,
  Typography,
  Grid,
  Card,
  CardContent,
} from '@mui/material';

// --- Componente FinancialNewsTicker (sin cambios) ---
function FinancialNewsTicker() {
  const [headlines, setHeadlines] = useState([]);

  useEffect(() => {
    async function fetchNews() {
      try {
        const res = await fetch(
          `https://newsapi.org/v2/everything?domains=wsj.com&apiKey=8783ccc2db0f4e4eb6f27389ad4b3273`
        );
        const data = await res.json();
        setHeadlines(data.articles ? data.articles.map((a) => a.title) : []);
      } catch (err) {
        console.error(err);
        setHeadlines(["No se pudieron cargar las noticias financieras."]);
      }
    }
    fetchNews();
  }, []);

  const tickerContent = [...headlines, ...headlines];

  return (
    <Box sx={{
      overflow: 'hidden',
      bgcolor: 'primary.dark',
      color: 'white',
      py: 1
    }}>
      <Box
        sx={{
          display: 'inline-block',
          whiteSpace: 'nowrap',
          animation: 'ticker 40s linear infinite',
          '&:hover': {
             animationPlayState: 'paused'
          }
        }}
      >
        {tickerContent.map((text, idx) => (
          <Typography key={idx} variant="body2" component="span" sx={{ mx: 4 }}>
            {text}
          </Typography>
        ))}
      </Box>
      <style>
        {`
          @keyframes ticker {
            0%   { transform: translateX(0%); }
            100% { transform: translateX(-50%); }
          }
        `}
      </style>
    </Box>
  );
}


// --- Componente Principal Admin ---
const drawerWidth = 240;
const appBarHeight = 64;
const newsTickerHeight = 40;

// 2. Definir los elementos del menú con sus rutas correspondientes
const menuItems = [
    { text: 'Crear Empresas', path: '/RegisterCompanies' },
    { text: 'Crear Proyectos', path: '/Addproyects' },
    // El botón de reportes está deshabilitado hasta que se cree su ruta
    { text: 'Ver y Descargar Reportes', path: '/reports', disabled: true },
];

export default function Admin() {
  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />

      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <FinancialNewsTicker />
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Panel del Administrador
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: 'border-box',
            top: `${appBarHeight + newsTickerHeight}px`
          },
        }}
      >
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {/* 3. Mapear el array de menuItems para crear los botones de navegación */}
            {menuItems.map((item) => (
              <ListItem key={item.text} disablePadding>
                 <ListItemButton
                    component={RouterLink}
                    to={item.path}
                    disabled={item.disabled || false} // Aplica el estado deshabilitado
                 >
                   <ListItemText primary={item.text} />
                 </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      <Box
        component="main"
        sx={{
            flexGrow: 1,
            p: 3,
            mt: `${(appBarHeight + newsTickerHeight) / 8}px`,
         }}
      >
        {/* El contenido de bienvenida se mantiene aquí porque esta es la página /Admin */}
        <Typography variant="h4" gutterBottom>
          Bienvenido al Panel de Administración
        </Typography>


        {/* Contenedor de tarjetas con mayor espaciado */}
        <Grid container spacing={4}>
          {/* Tarjeta 1 */}
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', backgroundColor: '#f5f5f5' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>Tip: Automatización</Typography>
                <Typography variant="body2">
                  El 40% del tiempo de un trabajador se pierde en tareas repetitivas. La automatización de procesos es clave para recuperar eficiencia y enfocarse en lo importante.
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Tarjeta 2 */}
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', backgroundColor: '#e3f2fd' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>Dato: Metas Claras</Typography>
                <Typography variant="body2">
                  Los equipos que establecen y revisan metas semanales tienen un 78% más de probabilidades de alcanzar sus objetivos principales a largo plazo.
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Tarjeta 3 */}
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', backgroundColor: '#f0f4c3' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>Tip: Comunicación</Typography>
                <Typography variant="body2">
                  Mejorar la claridad y frecuencia de la comunicación en un equipo puede incrementar la productividad general hasta en un 25%. ¡Las reuniones efectivas son oro!
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
}