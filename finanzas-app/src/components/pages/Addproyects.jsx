import React, { useEffect, useState } from 'react';
import {
  TextField,
  MenuItem,
  Button,
  Typography,
  Snackbar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Container,
  Alert,
} from '@mui/material';

const CrearProyecto = () => {
  const [empresas, setEmpresas] = useState([]);
  const [form, setForm] = useState({
    empresa_id: '',
    nombre: '',
    fecha_creacion: '',
    capital_inicial: '',
  });

  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success',
  });

  const [openDialog, setOpenDialog] = useState(false);

  // Cargar empresas
useEffect(() => {
  fetch('http://127.0.0.1:5000/reportes/empresas')
    .then((res) => res.json())
    .then((data) => setEmpresas(data.empresas)) // <- Aquí cambia a data.empresas
    .catch(() => setEmpresas([]));
}, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const validateForm = () => {
    return (
      form.empresa_id !== '' &&
      form.nombre.trim() !== '' &&
      form.fecha_creacion.trim() !== '' &&
      form.capital_inicial !== ''
    );
  };

  const handleOpenDialog = () => {
    if (!validateForm()) {
      setSnackbar({
        open: true,
        message: 'Todos los campos deben de ser llenados',
        severity: 'error',
      });
      return;
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSubmit = async () => {
    console.log('Datos enviados al servidor:', form);
    try {
      const res = await fetch('http://127.0.0.1:5000/reportes/crear/proyecto', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (res.ok) {
        setSnackbar({
          open: true,
          message: 'Proyecto creado exitosamente',
          severity: 'success',
        });
        setForm({
          empresa_id: '',
          nombre: '',
          fecha_creacion: '',
          capital_inicial: '',
        });
      } else {
        setSnackbar({
          open: true,
          message: 'Error al crear el proyecto',
          severity: 'error',
        });
      }
    } catch (error) {
      console.error('Error al enviar datos:', error);
      setSnackbar({
        open: true,
        message: 'Error al crear el proyecto',
        severity: 'error',
      });
    } finally {
      setOpenDialog(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h5" gutterBottom>Crear Proyecto</Typography>

<TextField
  select
  fullWidth
  label="Empresa"
  name="empresa_id"
  value={form.empresa_id}
  onChange={handleChange}
  margin="normal"
>
  {empresas.length === 0 ? (
    <MenuItem value="" disabled>
      No se pudieron obtener las empresas
    </MenuItem>
  ) : (
    empresas.map((empresa) => (
      <MenuItem key={empresa.id} value={empresa.id}>
        {empresa.nombre}
      </MenuItem>
    ))
  )}
</TextField>


      <TextField
        fullWidth
        label="Nombre del Proyecto"
        name="nombre"
        value={form.nombre}
        onChange={handleChange}
        margin="normal"
      />

      <TextField
        fullWidth
        type="date"
        label="Fecha de Creación"
        name="fecha_creacion"
        value={form.fecha_creacion}
        onChange={handleChange}
        margin="normal"
        InputLabelProps={{ shrink: true }}
      />

      <TextField
        fullWidth
        type="number"
        label="Capital Inicial"
        name="capital_inicial"
        value={form.capital_inicial}
        onChange={handleChange}
        margin="normal"
      />

      <Button
        variant="contained"
        color="primary"
        onClick={handleOpenDialog}
        sx={{ mt: 2 }}
      >
        Crear Proyecto
      </Button>

      {/* Diálogo de confirmación */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Confirmar creación</DialogTitle>
        <DialogContent>
          ¿Estás seguro de que deseas crear este proyecto?
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancelar</Button>
          <Button onClick={handleSubmit} variant="contained" color="primary">
            Confirmar
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar con Alert */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default CrearProyecto;
