import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
  Alert,
  Paper,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from '@mui/material';

const tipoBienOpciones = [
  { label: 'Efectivo y Equivalentes', value: 'EFECTIVO_Y_EQUIVALENTES' },
  { label: 'Bienes Inmuebles', value: 'BIENES_INMUEBLES' },
  { label: 'Muebles y Equipos', value: 'MUEBLES_Y_EQUIPOS' },
  { label: 'Inventario', value: 'INVENTARIO' },
  { label: 'Cuentas por Cobrar', value: 'CUENTAS_POR_COBRAR' },
  { label: 'Gasto', value: 'GASTO' },
];

export default function AdquisicionForm() {
  const [form, setForm] = useState({
    empresa_id: '',
    proyecto_id: '',
    nombre_bien: '',
    tipo_bien: '',
    desc_tipo_bien: '',
    monto_total: '',
    monto_inicial: '',
    fecha_adquisicion: '',
    forma_pago_char: '',
    meses_pago: '',
    numero_pagos: '',
    tiene_financiamiento: 'No',
    fuente_financiamiento: '',
    porcentaje_financiamiento: '',
    monto_financiado: '',
  });

  const [empresas, setEmpresas] = useState([]);
  const [proyectos, setProyectos] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [error, setError] = useState('');
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarErrorOpen, setSnackbarErrorOpen] = useState(false);


useEffect(() => {
  fetch('http://127.0.0.1:5000/reportes/empresas')
    .then((res) => res.json())
    .then((data) => setEmpresas(data.empresas)) // <- Aquí cambia a data.empresas
    .catch(() => setEmpresas([]));
}, []);

  useEffect(() => {
    if (form.empresa_id) {
      fetch(`http://127.0.0.1:5000/empresas/${form.empresa_id}/proyectos`)
        .then((res) => res.json())
        .then((data) => setProyectos(data))
        .catch(() => setProyectos([]));
    }
  }, [form.empresa_id]);

const handleChange = (e) => {
  const { name, value } = e.target;

  let updatedForm = { ...form, [name]: value };

  if (name === 'tiene_financiamiento' && value === 'No') {
    updatedForm = {
      ...updatedForm,
      fuente_financiamiento: 'NA',
      porcentaje_financiamiento: '0',
      numero_pagos: '0',
      monto_financiado: '0',
    };
  }

  setForm(updatedForm);
};


  const validateForm = () => {
    const camposObligatorios = [
      'empresa_id',
      'proyecto_id',
      'nombre_bien',
      'tipo_bien',
      'desc_tipo_bien',
      'monto_total',
      'monto_inicial',
      'fecha_adquisicion',
      'forma_pago_char',
      'meses_pago',
      'numero_pagos',
    ];

    for (const campo of camposObligatorios) {
      if (!form[campo]) return false;
    }

    if (form.tiene_financiamiento === 'Sí') {
      const camposFinanciamiento = [
        'fuente_financiamiento',
        'porcentaje_financiamiento',
        'monto_financiado',
      ];
      for (const campo of camposFinanciamiento) {
        if (!form[campo]) return false;
      }
    }

    return true;
  };

  const handleSubmit = () => {
    if (!validateForm()) {
      setError('Todos los campos obligatorios deben estar llenos.');
      return;
    }
    setError('');
    setOpenDialog(true);
  };

  const confirmSubmit = async () => {
    setOpenDialog(false);
    const dataToSend = {
      ...form,
      tiene_financiamiento: form.tiene_financiamiento === 'Sí',
    };
    try {
      const res = await fetch('http://127.0.0.1:5000/nueva/adquisicion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
      });
      if (res.ok) {
        setSnackbarOpen(true);
        setForm({
          empresa_id: '',
          proyecto_id: '',
          nombre_bien: '',
          tipo_bien: '',
          desc_tipo_bien: '',
          monto_total: '',
          monto_inicial: '',
          fecha_adquisicion: '',
          forma_pago_char: '',
          meses_pago: '',
          numero_pagos: '',
          tiene_financiamiento: 'No',
          fuente_financiamiento: '',
          porcentaje_financiamiento: '',
          monto_financiado: '',
        });
      } else {
        setSnackbarErrorOpen(true);
      }
    } catch (err) {
      console.error('Error al enviar datos:', err);
      setSnackbarErrorOpen(true);
    }
  };

const renderTextField = (field) => {
  const hiddenIfNoFinanciamiento = ['fuente_financiamiento', 'porcentaje_financiamiento', 'monto_financiado'];
  const disabledIfNoFinanciamiento = ['numero_pagos'];

  if (form.tiene_financiamiento === 'No' && hiddenIfNoFinanciamiento.includes(field)) {
    return null;
  }

  return (
    <Grid item xs={12} md={4} key={field}>
      <TextField
        fullWidth
        type={field.includes('fecha') ? 'date' : 'text'}
        name={field}
        label={field.replaceAll('_', ' ').toUpperCase()}
        value={form[field]}
        onChange={handleChange}
        InputLabelProps={field.includes('fecha') ? { shrink: true } : {}}
        disabled={form.tiene_financiamiento === 'No' && disabledIfNoFinanciamiento.includes(field)}
      />
    </Grid>
  );
};


  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Paper elevation={6} sx={{ p: 4, borderRadius: 4 }}>
        <Typography variant="h4" fontWeight={700} align="center" gutterBottom>
          Registro de Adquisición
        </Typography>
        <Grid container spacing={7}>
            <Grid item xs={12} md={6}>
               <FormControl fullWidth sx={{ minWidth: 200 }}>
                <InputLabel id="empresa-label">Empresa</InputLabel>
                <Select
                    labelId="empresa-label"
                    name="empresa_id"
                    value={form.empresa_id}
                    onChange={handleChange}
                    label="Empresa"
                >
                {empresas.length ? (
  empresas.map((e) => (
    <MenuItem key={e.empresa_id} value={e.empresa_id}>
      {e.nombre}
    </MenuItem>
  ))
) : (
  <MenuItem disabled>Error en servidor, no se pudieron cargar los datos</MenuItem>
)}

              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={6}>
                <FormControl fullWidth sx={{ minWidth: 200 }}>
              <InputLabel>Proyecto</InputLabel>
              <Select name="proyecto_id" value={form.proyecto_id} onChange={handleChange}>
                {proyectos.length ? (
                  proyectos.map((p) => <MenuItem key={p.id} value={p.id}>{p.nombre}</MenuItem>)
                ) : (
                  <MenuItem disabled>Error en servidor, no se pudieron cargar los datos</MenuItem>
                )}
              </Select>
            </FormControl>
          </Grid>

            {[
            'nombre_bien',
            'desc_tipo_bien',
            'monto_total',
            'monto_inicial',
            'fecha_adquisicion',
            'forma_pago_char',
            'meses_pago'
             ].map(renderTextField)}

          <Grid item xs={12} md={6}>
                <FormControl fullWidth sx={{ minWidth: 200 }}>
              <InputLabel>Tipo de Bien</InputLabel>
              <Select name="tipo_bien" value={form.tipo_bien} onChange={handleChange}>
                {tipoBienOpciones.map((op) => (
                  <MenuItem key={op.value} value={op.value}>{op.label}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

                <Grid item xs={12} md={6}>
        <FormControl fullWidth sx={{ minWidth: 200 }}>
            <InputLabel id="financiamiento-label">¿Tiene Financiamiento?</InputLabel>
            <Select
            labelId="financiamiento-label"
            name="tiene_financiamiento"
            value={form.tiene_financiamiento}
            onChange={handleChange}
            label="¿Tiene Financiamiento?"
            >
            <MenuItem value="Sí">Sí</MenuItem>
            <MenuItem value="No">No</MenuItem>
            </Select>
        </FormControl>
        </Grid>

        </Grid>

        {error && (
          <Box mt={2}>
            <Alert severity="error">{error}</Alert>
          </Box>
        )}
{form.tiene_financiamiento === 'Sí' && (
  <Grid container spacing={7} mt={7}>
    {['numero_pagos', 'fuente_financiamiento', 'porcentaje_financiamiento', 'monto_financiado'].map(renderTextField)}
  </Grid>
)}


        <Box mt={4} textAlign="center">
          <Button variant="contained" color="primary" size="large" onClick={handleSubmit}>
            Enviar Formulario
          </Button>
        </Box>
      </Paper>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>¿Confirmar Envío?</DialogTitle>
        <DialogContent>
          <Typography>¿Estás seguro de que deseas enviar estos datos?</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancelar</Button>
          <Button onClick={confirmSubmit} variant="contained" color="primary">Confirmar</Button>
        </DialogActions>
      </Dialog>

      <Snackbar open={snackbarOpen} autoHideDuration={4000} onClose={() => setSnackbarOpen(false)} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}>
        <Alert onClose={() => setSnackbarOpen(false)} severity="success" sx={{ width: '100%' }}>
          ¡Formulario enviado correctamente!
        </Alert>
      </Snackbar>

      <Snackbar open={snackbarErrorOpen} autoHideDuration={4000} onClose={() => setSnackbarErrorOpen(false)} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}>
        <Alert onClose={() => setSnackbarErrorOpen(false)} severity="error" sx={{ width: '100%' }}>
          Hubo un error al enviar el formulario. Intenta de nuevo.
        </Alert>
      </Snackbar>
    </Container>
  );
}
