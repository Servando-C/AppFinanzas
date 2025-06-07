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

    function ProjectRegister() {
    const [form, setForm] = useState({
        nombre: "",
        fechaCreacion: "",
        capital: "",
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

        // Validación para el capital (debe ser un número positivo)
        const capitalRegex = /^[0-9]+(\.[0-9]{1,2})?$/;
        if (form.capital && !capitalRegex.test(form.capital)) {
        newErrors.capital = "Capital no válido (número positivo).";
        }

        // Validación para la fecha
        if (form.fechaCreacion && isNaN(new Date(form.fechaCreacion))) {
        newErrors.fechaCreacion = "Fecha no válida.";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async () => {
        console.log("Datos enviados:", form);
        if (!validateFields()) return;

        try {
        const res = await fetch("http://127.0.0.1:5000/proyectos/crear", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(form),
        });

        if (res.ok) {
            setSuccessOpen(true);
            setForm({
            nombre: "",
            fechaCreacion: "",
            capital: "",
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
        <Container maxWidth="sm" sx={{ py: 8 }}>
            <Typography variant="h4" gutterBottom align="center" fontWeight={700}>
            Registro de Proyecto
            </Typography>

            {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
                {error}
            </Alert>
            )}

            <Box component="form" noValidate autoComplete="off">
            {[ 
                { name: "nombre", label: "Nombre del Proyecto" },
                { name: "fechaCreacion", label: "Fecha de Creación", type: "date" },
                { name: "capital", label: "Capital Disponible", type: "number" }
            ].map(({ name, label, type }) => (
                <TextField
                key={name}
                fullWidth
                margin="normal"
                label={label}
                name={name}
                type={type || "text"}
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
            message="Proyecto registrado correctamente"
        />
        </Box>
    );
}

export default ProjectRegister;
