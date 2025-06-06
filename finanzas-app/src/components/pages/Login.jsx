import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Checkbox from '@mui/material/Checkbox';
import CssBaseline from '@mui/material/CssBaseline';
import FormControlLabel from '@mui/material/FormControlLabel';
import Divider from '@mui/material/Divider';
import FormLabel from '@mui/material/FormLabel';
import FormControl from '@mui/material/FormControl';
import Link from '@mui/material/Link';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import MuiCard from '@mui/material/Card';
import { styled } from '@mui/material/styles';
import AppTheme from '../../theme/AppTheme';
import ColorModeSelect from '../../theme/ColorModeSelect';
import WebhookIcon from '@mui/icons-material/Webhook';
import ForgotPassword from '../layout/ForgotPassword';
import GoogleIcon from '@mui/icons-material/Google';
import FacebookIcon from '@mui/icons-material/Facebook';
import { useNavigate } from 'react-router-dom'; // 1. IMPORTANTE: Añade useNavigate para la redirección

const Card = styled(MuiCard)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignSelf: 'center',
  width: '100%',
  padding: theme.spacing(4),
  gap: theme.spacing(2),
  margin: 'auto',
  [theme.breakpoints.up('sm')]: {
    maxWidth: '450px',
  },
  boxShadow:
    'hsla(220, 30%, 5%, 0.05) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.05) 0px 15px 35px -5px',
  ...theme.applyStyles('dark', {
    boxShadow:
      'hsla(220, 30%, 5%, 0.5) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.08) 0px 15px 35px -5px',
  }),
}));

const SignInContainer = styled(Stack)(({ theme }) => ({
  height: 'calc((1 - var(--template-frame-height, 0)) * 100dvh)',
  minHeight: '100%',
  padding: theme.spacing(2),
  [theme.breakpoints.up('sm')]: {
    padding: theme.spacing(4),
  },
  '&::before': {
    content: '""',
    display: 'block',
    position: 'absolute',
    zIndex: -1,
    inset: 0,
    backgroundImage:
      'radial-gradient(ellipse at 50% 50%, hsl(210, 100%, 97%), hsl(0, 0%, 100%))',
    backgroundRepeat: 'no-repeat',
    ...theme.applyStyles('dark', {
      backgroundImage:
        'radial-gradient(at 50% 50%, hsla(210, 100%, 16%, 0.5), hsl(220, 30%, 5%))',
    }),
  },
}));

export default function Login(props) {
  const [emailError, setEmailError] = React.useState(false);
  const [emailErrorMessage, setEmailErrorMessage] = React.useState('');
  const [passwordError, setPasswordError] = React.useState(false);
  const [passwordErrorMessage, setPasswordErrorMessage] = React.useState('');
  const [open, setOpen] = React.useState(false);
  
  // 2. IMPORTANTE: Inicializa la función de navegación
  const navigate = useNavigate();

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };
  
  // 3. --- FUNCIÓN handleSubmit CORREGIDA ---
  const handleSubmit = (event) => {
    // Previene que la página se recargue, como ya lo hacías
    event.preventDefault();
    
    // Obtener los datos del formulario. Esto está bien para leer los valores.
    const formData = new FormData(event.currentTarget);
    const email = formData.get('email');
    const password = formData.get('password');

    // Aquí podrías poner tu lógica de validación como la tenías
    let isValid = true;
    if (!email || !/\S+@\S+\.\S+/.test(email)) {
      setEmailError(true);
      setEmailErrorMessage('Por favor, ingresa un correo válido.');
      isValid = false;
    } else {
      setEmailError(false);
      setEmailErrorMessage('');
    }
    if (!password) { // Añadí una validación simple de contraseña
      setPasswordError(true);
      setPasswordErrorMessage('La contraseña no puede estar vacía.');
      isValid = false;
    } else {
      setPasswordError(false);
      setPasswordErrorMessage('');
    }
    if (!isValid) return;

    // Crear el objeto payload que espera tu backend.
    // La clave 'correo' debe coincidir con data.get('correo') en tu endpoint de Flask.
    const payload = {
      correo: email,
      password: password,
    };

    // Hacer la llamada a la API usando fetch
    fetch('http://127.0.0.1:5000/auth/login', { // Asegúrate que esta URL y puerto sean correctos
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // <-- El header crucial que resuelve el error 415
      },
      body: JSON.stringify(payload), // <-- Convierte tu objeto a una cadena JSON
    })
    .then(response => {
      // Si la respuesta no es 2xx, la procesamos como un error
      if (!response.ok) {
        return response.json().then(err => { throw new Error(err.msg || 'Error en el login'); });
      }
      return response.json(); // Si es 2xx, procesamos el JSON de éxito
    })
    .then(data => {
      // Éxito: tienes el token de acceso
      console.log('Login exitoso:', data);
      
      // Guardar el token para usarlo en futuras peticiones
      localStorage.setItem('access_token', data.access_token);
      
      // Redirigir al usuario al dashboard o página principal
      navigate('/Form'); // Asegúrate de tener una ruta '/dashboard' definida
    })
    .catch(error => {
      // Manejar errores de red o errores de la API (ej. 401 Credenciales incorrectas)
      console.error('Error:', error.message);
      // Aquí podrías mostrar un mensaje de error al usuario
      setPasswordError(true);
      setEmailError(true);
      setEmailErrorMessage(error.message); // Muestra el mensaje de error del backend
    });
  };

  // La validación ahora puede ser parte de handleSubmit o llamarse desde ahí.
  // He movido la lógica de validación dentro de handleSubmit para simplificar.

  return (
    <AppTheme {...props}>
      <CssBaseline enableColorScheme />
      <SignInContainer direction="column" justifyContent="space-between">
        <ColorModeSelect sx={{ position: 'fixed', top: '1rem', right: '1rem' }} />
        <Card variant="outlined">
          <WebhookIcon />
          <Typography
            component="h1"
            variant="h4"
            sx={{ width: '100%', fontSize: 'clamp(2rem, 10vw, 2.15rem)' }}
          >
            Sign in
          </Typography>
          <Box
            component="form"
            onSubmit={handleSubmit}
            noValidate
            sx={{
              display: 'flex',
              flexDirection: 'column',
              width: '100%',
              gap: 2,
            }}
          >
            <FormControl>
              <FormLabel htmlFor="email">Email</FormLabel>
              <TextField
                error={emailError}
                helperText={emailErrorMessage}
                id="email"
                type="email"
                name="email" // 'name' es importante para que FormData lo pueda leer
                placeholder="your@email.com"
                autoComplete="email"
                autoFocus
                required
                fullWidth
                variant="outlined"
                color={emailError ? 'error' : 'primary'}
              />
            </FormControl>
            <FormControl>
              <FormLabel htmlFor="password">Password</FormLabel>
              <TextField
                error={passwordError}
                helperText={passwordErrorMessage}
                name="password" // 'name' es importante
                placeholder="••••••"
                type="password"
                id="password"
                autoComplete="current-password"
                required
                fullWidth
                variant="outlined"
                color={passwordError ? 'error' : 'primary'}
              />
            </FormControl>
            <FormControlLabel
              control={<Checkbox value="remember" name="remember" color="primary" />}
              label="Remember me"
            />
            <ForgotPassword open={open} handleClose={handleClose} />
            <Button
              type="submit"
              fullWidth
              variant="contained"
            >
              Sign in
            </Button>
            <Link
              component="button"
              type="button"
              onClick={handleClickOpen}
              variant="body2"
              sx={{ alignSelf: 'center' }}
            >
              Forgot your password?
            </Link>
          </Box>
          <Divider>or</Divider>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography sx={{ textAlign: 'center' }}>
              Don&apos;t have an account?{' '}
              <Link
                href="/signup" // Asegúrate de tener una ruta de registro
                variant="body2"
                sx={{ alignSelf: 'center' }}
              >
                Sign up
              </Link>
            </Typography>
          </Box>
        </Card>
      </SignInContainer>
    </AppTheme>
  );
}