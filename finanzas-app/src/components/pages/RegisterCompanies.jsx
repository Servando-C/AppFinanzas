import React, { useState } from "react";
import {
  Box,
  Typography,
  Container,
  TextField,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
  Alert,
} from "@mui/material";

function FinancialNewsTicker() {
  const [headlines, setHeadlines] = useState([]);

  React.useEffect(() => {
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
    <Box sx={{ overflow: "hidden", bgcolor: "#0d47a1", color: "white", py: 1 }}>
      <Box
        sx={{
          display: "inline-block",
          whiteSpace: "nowrap",
          animation: "ticker 100s linear infinite",
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
            0%   { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
          }
        `}
      </style>
    </Box>
  );
}

export default function RegisterCompanies() {
  const [form, setForm] = useState({
    nombre: "",
    dueno: "",
    correo: "",
    telefono: "",
    direccion: "",
    rfc: "",
  });

  const [errors, setErrors] = useState({});
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [successOpen, setSuccessOpen] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors((prev) => ({ ...prev, [e.target.name]: "" }));
    setError("");
  };

  const validateFields = () => {
    const newErrors = {};
    for (const key in form) {
      if (form[key].trim() === "") {
        newErrors[key] = "Este campo es obligatorio.";
      }
    }

    const correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (form.correo && !correoRegex.test(form.correo)) {
      newErrors.correo = "Correo electrónico no válido.";
    }

    const telefonoRegex = /^[0-9]{7,15}$/;
    if (form.telefono && !telefonoRegex.test(form.telefono)) {
      newErrors.telefono = "Teléfono inválido (solo números, 7-15 dígitos).";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    console.log("Datos enviados:", form);
    if (!validateFields()) return;

    try {
      const res = await fetch("http://127.0.0.1:5000/api/reportes/crear/empresa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (res.ok) {
        setSuccessOpen(true);
        setForm({
          nombre: "",
          dueno: "",
          correo: "",
          telefono: "",
          direccion: "",
          rfc: "",
        });
        setErrors({});
        setError("");
      } else {
        setError("Hubo un error al enviar los datos al servidor.");
      }
    } catch (err) {
      console.error("Error:", err);
      setError("No se pudo conectar con el servidor.");
    } finally {
      setConfirmOpen(false);
    }
  };

  return (
    <Box sx={{ background: "#f5f7fa", minHeight: "100vh" }}>
      <FinancialNewsTicker />
      <Container maxWidth="sm" sx={{ py: 8 }}>
        <Typography variant="h4" gutterBottom align="center" fontWeight={700}>
          Registro de Empresa
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box component="form" noValidate autoComplete="off">
          {[
            { name: "nombre", label: "Nombre" },
            { name: "dueno", label: "Dueño" },
            { name: "correo", label: "Correo" },
            { name: "telefono", label: "Teléfono" },
            { name: "direccion", label: "Dirección" },
            { name: "rfc", label: "RFC" },
          ].map(({ name, label }) => (
            <TextField
              key={name}
              fullWidth
              margin="normal"
              label={label}
              name={name}
              value={form[name]}
              onChange={handleChange}
              error={Boolean(errors[name])}
              helperText={errors[name]}
            />
          ))}
          <Box textAlign="center" mt={3}>
            <Button
              variant="contained"
              color="primary"
              onClick={() => {
                if (validateFields()) setConfirmOpen(true);
              }}
            >
              Enviar
            </Button>
          </Box>
        </Box>
      </Container>

      <Dialog open={confirmOpen} onClose={() => setConfirmOpen(false)}>
        <DialogTitle>¿Estás seguro?</DialogTitle>
        <DialogContent>¿Seguro que los datos son correctos?</DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmOpen(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleSubmit}>
            Enviar
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={successOpen}
        autoHideDuration={3000}
        onClose={() => setSuccessOpen(false)}
        message="Datos enviados correctamente"
      />
    </Box>
  );
}
