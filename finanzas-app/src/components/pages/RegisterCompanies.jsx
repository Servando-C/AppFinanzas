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

// Ticker de noticias
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
          animation: "ticker 120s linear infinite",
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

  const [confirmOpen, setConfirmOpen] = useState(false);
  const [successOpen, setSuccessOpen] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError(""); // Limpiar error al escribir
  };

  const validateFields = () => {
    for (const key in form) {
      if (form[key].trim() === "") {
        setError("Por favor completa todos los campos antes de enviar.");
        return false;
      }
    }
    return true;
  };

  const handleSubmit = async () => {
    console.log("Datos enviados:", form);
    if (!validateFields()) return;

    try {
      const res = await fetch("http://localhost:4000/api/empresas", {
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
          {["nombre", "dueno", "correo", "telefono", "direccion", "rfc"].map((field) => (
            <TextField
              key={field}
              fullWidth
              margin="normal"
              label={field.charAt(0).toUpperCase() + field.slice(1)}
              name={field}
              value={form[field]}
              onChange={handleChange}
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

      {/* Diálogo de confirmación */}
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

      {/* Notificación de éxito */}
      <Snackbar
        open={successOpen}
        autoHideDuration={3000}
        onClose={() => setSuccessOpen(false)}
        message="Datos enviados correctamente"
      />
    </Box>
  );
}
