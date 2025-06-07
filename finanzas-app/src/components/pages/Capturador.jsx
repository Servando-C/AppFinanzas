import React, { useEffect, useState } from 'react';
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

// --- Componente FinancialNewsTicker (se mantiene igual) ---
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
        setHeadlines(["Las noticias no están disponibles en este momento."]);
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

// --- Componente Principal para el Capturista ---
const drawerWidth = 240;
const appBarHeight = 64;
const newsTickerHeight = 40;

// Menú lateral actualizado para el Capturista
const menuItems = [
    { text: 'Acerca de Nosotros', path: '/' },
    { text: 'Capturar Adquisiciones', path: '/Adquisicions' },
];

export default function Capturador() {
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
            Panel del Capturista
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
            {menuItems.map((item) => (
              <ListItem key={item.text} disablePadding>
                 <ListItemButton
                    component={RouterLink}
                    to={item.path}
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
        {/* Mensaje de bienvenida y tarjetas con datos felices */}
        <Typography variant="h4" gutterBottom>
          ¡Que tengas un excelente día Capturista!
        </Typography>

{/* Contenedor de tarjetas con mayor espaciado */}
<Grid container spacing={4} alignItems="stretch">
      {/* Tarjeta 1 */}
  <Grid item xs={12} md={4}>
    <Card sx={{ height: '100%', backgroundColor: '#f5f5f5' }}>
      <CardContent  sx={{ minHeight: 120 }}>
        <Typography variant="h6" gutterBottom>Dato Feliz: Poder de la Sonrisa</Typography>
        <Typography variant="body2">
          ¡Sonreír puede mejorar tu estado de ánimo y reducir el estrés! Estudios demuestran que una sonrisa sincera libera endorfinas, haciéndote sentir más feliz.
        </Typography>
      </CardContent>
    </Card>
  </Grid>

  {/* Tarjeta 2 */}
  <Grid item xs={12} md={4}>
    <Card sx={{ height: '100%', backgroundColor: '#e3f2fd' }}>
      <CardContent  sx={{ minHeight: 120 }}>
        <Typography variant="h6" gutterBottom>Alegría: Pequeños Gestos</Typography>
        <Typography variant="body2">
          Ayudar a otros, incluso con pequeños gestos, activa el centro de recompensa del cerebro, generando una sensación de felicidad y propósito.
        </Typography>
      </CardContent>
    </Card>
  </Grid>

  {/* Tarjeta 3 */}
  <Grid item xs={12} md={4}>
    <Card sx={{ height: '100%', backgroundColor: '#f0f4c3' }}>
      <CardContent  sx={{ minHeight: 120 }} >
        <Typography variant="h6" gutterBottom>Optimismo: Sueños Cumplidos</Typography>
        <Typography variant="body2">
          Visualizar tus metas alcanzadas y celebrar cada pequeño avance te acerca a tus sueños y llena tu día de optimismo y energía.
        </Typography>
      </CardContent>
    </Card>
  </Grid>
</Grid>

      </Box>
    </Box>
  );
}