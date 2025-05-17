// src/components/pages/Login.jsx
import React from 'react';
import { Box, Container, Typography, TextField, Button, InputAdornment } from '@mui/material';
import { AccountCircle, Lock } from '@mui/icons-material';

const Login = () => {
  return (
    <Box
      sx={{
        backgroundImage: "url('https://images.pexels.com/photos/5561913/pexels-photo-5561913.jpeg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        overflow: 'hidden',
        '&::before': {
          content: '""',
          position: 'absolute',
          inset: 0,
          backgroundColor: 'rgba(0,0,0,0.6)',
          zIndex: 1
        }
      }}
    >
      <Container
        maxWidth="xs"
        sx={{

          padding: 4,
          borderRadius: 4,
          boxShadow: 4,
          position: 'relative',
          zIndex: 2,
        }}
      >
        <Typography variant="h4" fontWeight="bold" align="center" gutterBottom color='white'>
          Bienvenido a EcoBalance
        </Typography>
        <Typography variant="body1" align="center" mb={3} color='white'>
          Gestiona tus finanzas con equilibrio y claridad.
        </Typography>

        <TextField
          label="Usuario"
          color='black'
          variant="outlined"
          fullWidth
          margin="normal"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <AccountCircle />
              </InputAdornment>
            ),
          }}
        />
        <TextField
          label="Contraseña"
          type="password"
          variant="outlined"
          fullWidth
          margin="normal"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Lock />
              </InputAdornment>
            ),
          }}
        />
        <Button variant="contained" fullWidth sx={{ mt: 2, backgroundColor: '#2F5D62', '&:hover': { backgroundColor: '#3b7a78' } }}>
          Ingresar
        </Button>
      </Container>
    </Box>
  );
};

export default Login;
