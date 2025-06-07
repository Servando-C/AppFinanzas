import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Container,
  Typography,
  Grid,
  Paper,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  CircularProgress,
  Stack,
  Fade,
} from '@mui/material';
import { Download, Business, Assignment, CalendarToday } from '@mui/icons-material';

export default function Reports() {
  const [form, setForm] = useState({
    empresa_id: '',
    proyecto_id: '',
  });

  const [empresas, setEmpresas] = useState([]);
  const [proyectos, setProyectos] = useState([]);
  const [fechas, setFechas] = useState([]);
  const [selectedFecha, setSelectedFecha] = useState('');

  // Estados de carga para una mejor UX
  const [loadingEmpresas, setLoadingEmpresas] = useState(false);
  const [loadingProyectos, setLoadingProyectos] = useState(false);
  const [loadingFechas, setLoadingFechas] = useState(false);

  // --- LÓGICA DE CARGA DE EMPRESAS ---
  useEffect(() => {
    setLoadingEmpresas(true);
    fetch('http://127.0.0.1:5000/reportes/empresas')
      .then((res) => res.json())
      .then((data) => setEmpresas(data.empresas || []))
      .catch((error) => {
        console.error('Error fetching empresas:', error);
        setEmpresas([]);
      })
      .finally(() => setLoadingEmpresas(false));
  }, []);

  // --- LÓGICA DE CARGA DE PROYECTOS ---
  useEffect(() => {
    if (!form.empresa_id) {
      setProyectos([]);
      setForm((prevForm) => ({ ...prevForm, proyecto_id: '' }));
      setFechas([]);
      setSelectedFecha('');
      return;
    }

    setLoadingProyectos(true);
    fetch(`http://127.0.0.1:5000/reportes/empresas/${form.empresa_id}/proyectos`)
      .then((res) => res.json())
      .then((data) => setProyectos(data.proyectos || []))
      .catch((error) => {
        console.error('Error fetching proyectos:', error);
        setProyectos([]);
      })
      .finally(() => setLoadingProyectos(false));
  }, [form.empresa_id]);

  // --- LÓGICA DE CARGA DE FECHAS ---
  useEffect(() => {
    if (form.empresa_id && form.proyecto_id) {
      setFechas([]);
      setSelectedFecha('');
      setLoadingFechas(true);

      fetch(`http://127.0.0.1:5000/reportes/tesoreria/fechas/${form.empresa_id}/${form.proyecto_id}`)
        .then((res) => res.json())
        .then((data) => {
          if (data.success && Array.isArray(data.fechas)) {
            setFechas(data.fechas);
          } else {
            setFechas([]);
          }
        })
        .catch((error) => {
          console.error('Error fetching fechas:', error);
          setFechas([]);
        })
        .finally(() => setLoadingFechas(false));
    } else {
      setFechas([]);
      setSelectedFecha('');
    }
  }, [form.empresa_id, form.proyecto_id]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === 'empresa_id') {
      setForm({ empresa_id: value, proyecto_id: '' });
      setSelectedFecha('');
    } else if (name === 'proyecto_id') {
      setForm((prevForm) => ({ ...prevForm, proyecto_id: value }));
      setSelectedFecha('');
    } else if (name === 'selectedFecha') {
      setSelectedFecha(value);
    }
  };

  const handleDownloadPdf = () => {
    if (!form.empresa_id || !form.proyecto_id || !selectedFecha) {
      alert('Por favor, seleccione una empresa, un proyecto y una fecha.');
      return;
    }
    const reportUrl = `http://127.0.0.1:5000/reportes/balance-general/pdf?empresa_id=${form.empresa_id}&proyecto_id=${form.proyecto_id}&fecha=${selectedFecha}`;
    window.open(reportUrl, '_blank');
  };

  const isDownloadButtonDisabled = !form.empresa_id || !form.proyecto_id || !selectedFecha;

  const renderSelectWithIcon = (icon, children) => (
    <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
      <Box sx={{ mr: 2, color: 'action.active' }}>{icon}</Box>
      {children}
    </Box>
  );

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        py: 6,
      }}
    >
      <Container maxWidth="sm">
        <Fade in={true} timeout={800}>
          <Paper
            elevation={12}
            sx={{
              p: { xs: 3, sm: 5 },
              borderRadius: '20px',
              backdropFilter: 'blur(10px)',
              backgroundColor: 'rgba(255, 255, 255, 0.8)',
              transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
              '&:hover': {
                transform: 'translateY(-5px)',
                boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
              },
            }}
          >
            <Typography
              variant="h4"
              fontWeight={800}
              align="center"
              gutterBottom
              sx={{
                background: 'linear-gradient(45deg, #0288d1 30%, #26c6da 90%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 4,
              }}
            >
              Generador de Reportes
            </Typography>

            <Stack spacing={4}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="empresa-label">Empresa</InputLabel>
                <Select
                  labelId="empresa-label"
                  name="empresa_id"
                  value={form.empresa_id}
                  onChange={handleChange}
                  label="Empresa"
                  startAdornment={<Business sx={{ mr: 1, color: 'action.active' }} />}
                >
                  {loadingEmpresas ? (
                    <MenuItem disabled sx={{ justifyContent: 'center' }}>
                      <CircularProgress size={24} />
                    </MenuItem>
                  ) : empresas.length > 0 ? (
                    empresas.map((e) => (
                      <MenuItem key={e.empresa_id} value={e.empresa_id}>
                        {e.nombre}
                      </MenuItem>
                    ))
                  ) : (
                    <MenuItem disabled>No hay empresas disponibles</MenuItem>
                  )}
                </Select>
              </FormControl>

              <FormControl fullWidth variant="outlined" disabled={!form.empresa_id || loadingProyectos}>
                <InputLabel>Proyecto</InputLabel>
                <Select
                  name="proyecto_id"
                  value={form.proyecto_id}
                  onChange={handleChange}
                  label="Proyecto"
                  startAdornment={<Assignment sx={{ mr: 1, color: 'action.active' }} />}
                >
                  {loadingProyectos ? (
                    <MenuItem disabled sx={{ justifyContent: 'center' }}>
                      <CircularProgress size={24} />
                    </MenuItem>
                  ) : proyectos.length > 0 ? (
                    proyectos.map((p) => (
                      <MenuItem key={p.proyecto_id} value={p.proyecto_id}>
                        {p.nombre}
                      </MenuItem>
                    ))
                  ) : (
                    <MenuItem disabled>
                      {form.empresa_id ? 'No hay proyectos' : 'Seleccione una empresa'}
                    </MenuItem>
                  )}
                </Select>
              </FormControl>

              <FormControl fullWidth variant="outlined" disabled={!form.proyecto_id || loadingFechas}>
                <InputLabel>Fecha</InputLabel>
                <Select
                  name="selectedFecha"
                  value={selectedFecha}
                  onChange={handleChange}
                  label="Fecha"
                  startAdornment={<CalendarToday sx={{ mr: 1, color: 'action.active' }} />}
                >
                  {loadingFechas ? (
                    <MenuItem disabled sx={{ justifyContent: 'center' }}>
                      <CircularProgress size={24} />
                    </MenuItem>
                  ) : fechas.length > 0 ? (
                    fechas.map((f) => (
                      <MenuItem key={f} value={f}>
                        {f}
                      </MenuItem>
                    ))
                  ) : (
                    <MenuItem disabled>
                      {form.proyecto_id ? 'No hay fechas' : 'Seleccione un proyecto'}
                    </MenuItem>
                  )}
                </Select>
              </FormControl>

              <Box pt={2} textAlign="center">
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleDownloadPdf}
                  disabled={isDownloadButtonDisabled}
                  startIcon={<Download />}
                  sx={{
                    borderRadius: '50px',
                    padding: '12px 30px',
                    fontWeight: 'bold',
                    background: isDownloadButtonDisabled
                      ? 'rgba(0, 0, 0, 0.12)'
                      : 'linear-gradient(45deg, #0288d1 30%, #26c6da 90%)',
                    color: 'white',
                    boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)',
                    transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                    '&:hover': {
                      transform: 'scale(1.05)',
                      boxShadow: '0 6px 20px rgba(0, 0, 0, 0.3)',
                    },
                  }}
                >
                  Descargar PDF
                </Button>
              </Box>
            </Stack>
          </Paper>
        </Fade>
      </Container>
    </Box>
  );
}