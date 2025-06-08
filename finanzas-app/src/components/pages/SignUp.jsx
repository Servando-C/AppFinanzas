import React, { useEffect, useState } from 'react';
import {
  Container, Typography, TextField, Button, MenuItem,
  Paper, Box
} from '@mui/material';

const SignUp = () => {
  const [empresas, setEmpresas] = useState([]);
  const [formData, setFormData] = useState({
    empresa_id: '',
    nombre: '',
    correo: '',
    rfc: '',
    password: ''
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
  fetch('http://127.0.0.1:5000/api/reportes/empresas')
      .then(response => response.json())
      .then(data => {
        setEmpresas(data.empresas);
      })
      .catch(error => {
        console.error('Error al obtener empresas:', error);
      });
  }, []);

  const validate = () => {
    const newErrors = {};
    for (const key in formData) {
      if (!formData[key]) {
        newErrors[key] = 'Este campo es obligatorio';
      }
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;

    fetch('http://127.0.0.1:5000/api/auth/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })
      .then(res => {
        if (res.ok) {
          alert('Usuario creado exitosamente');
        } else {
          alert('Error al crear el usuario');
        }
      })
      .catch(err => {
        console.error(err);
        alert('Error en la conexión');
      });
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4, borderRadius: 3 }}>
        <Typography variant="h5" gutterBottom>
          Crear Cuenta de Usuario
        </Typography>

        <Box component="form" onSubmit={handleSubmit} noValidate>
          <TextField
            select
            fullWidth
            label="Empresa"
            name="empresa_id"
            value={formData.empresa_id || ''}
            onChange={handleChange}
            margin="normal"
            error={!!errors.empresa_id}
            helperText={errors.empresa_id}
          >
            {empresas.length === 0 ? (
              <MenuItem value="" disabled>
                No se pudieron obtener las empresas
              </MenuItem>
            ) : (
              empresas.map((empresa) => (
                <MenuItem key={empresa.empresa_id} value={String(empresa.empresa_id)}>
                  {empresa.nombre}
                </MenuItem>
              ))
            )}
          </TextField>

          <TextField
            fullWidth
            name="nombre"
            label="Nombre"
            value={formData.nombre}
            onChange={handleChange}
            margin="normal"
            error={!!errors.nombre}
            helperText={errors.nombre}
          />

          <TextField
            fullWidth
            name="correo"
            label="Correo Electrónico"
            type="email"
            value={formData.correo}
            onChange={handleChange}
            margin="normal"
            error={!!errors.correo}
            helperText={errors.correo}
          />

          <TextField
            fullWidth
            name="rfc"
            label="RFC"
            value={formData.rfc}
            onChange={handleChange}
            margin="normal"
            error={!!errors.rfc}
            helperText={errors.rfc}
          />

          <TextField
            fullWidth
            name="password"
            label="Contraseña"
            type="password"
            value={formData.password}
            onChange={handleChange}
            margin="normal"
            error={!!errors.password}
            helperText={errors.password}
          />

          <Button
            variant="contained"
            color="primary"
            type="submit"
            fullWidth
            sx={{ mt: 3 }}
          >
            Registrarse
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default SignUp;
