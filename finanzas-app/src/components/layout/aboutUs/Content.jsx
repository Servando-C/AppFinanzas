import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import InputLabel from '@mui/material/InputLabel';
import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import visuallyHidden from '@mui/utils/visuallyHidden';
import { styled } from '@mui/material/styles';

export default function Content() {
  return (
    <Box>
      <Container
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          pt: { xs: 14, sm: 20 },
          pb: { xs: 8, sm: 12 },
        }}
      >
        <Stack
          spacing={2}
          useFlexGap
          sx={{ alignItems: 'center', width: { xs: '100%', sm: '70%' } }}
        >
          <Typography
            variant="h1"
            sx={{
              display: 'flex',
              flexDirection: { xs: 'column', sm: 'row' },
              alignItems: 'center',
              fontSize: 'clamp(3rem, 10vw, 3.5rem)',
            }}
          >
            The&nbsp;best&nbsp;way&nbsp;
            <Typography
              component="span"
              variant="h1"
              sx={(theme) => ({
                fontSize: 'inherit',
                color: 'primary.main',
                ...theme.applyStyles('dark', {
                  color: 'primary.light',
                }),
              })}
            >
              to do it
            </Typography>
          </Typography>
          <Typography
            sx={{
              textAlign: 'center',
              color: 'text.secondary',
              width: { sm: '100%', md: '80%' },
            }}
          >
            Explore our cutting-edge results statement generator, delivering high-quality solutions
            tailored to your needs. Elevate your experience with top-tier features
            and services.
          </Typography>
          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={1}
            useFlexGap
            sx={{ pt: 2, width: { xs: '100%', sm: '350px' } }}
          >
            <InputLabel htmlFor="email-hero" sx={visuallyHidden}>
              Email
            </InputLabel>
            <TextField
              id="email-hero"
              hiddenLabel
              size="small"
              variant="outlined"
              aria-label="Enter your email address"
              placeholder="Your email address"
              fullWidth
              slotProps={{
                htmlInput: {
                  autoComplete: 'off',
                  'aria-label': 'Enter your email address',
                },
              }}
            />
            <Button
              variant="contained"
              color="primary"
              size="small"
              sx={{ minWidth: 'fit-content' }}
            >
              Start now
            </Button>
          </Stack>
          <Typography
            variant="caption"
            color="text.secondary"
            sx={{ textAlign: 'center' }}
          >
            By clicking &quot;Start now&quot; you agree to our&nbsp;
            <Link href="#" color="primary">
              Terms & Conditions
            </Link>
            .
          </Typography>
        </Stack>
        <Stack
          spacing={6} // Espacio entre cada sección (Historia, Misión, Visión)
          sx={{
            width: { xs: '100%', md: '80%'}, // Ancho del bloque de contenido de estas secciones
            textAlign: 'left', // Alineación del texto para mejor legibilidad de párrafos
          }}
        >
          {/* Nuestra Historia */}
          <Box>
            <Typography
              variant="h4" // O h2, h3 según tu jerarquía semántica
              component="h2"
              sx={{
                fontWeight: 'bold',
                mb: 2, // Margen inferior para separar del párrafo
                textAlign: 'justify', // Título centrado
                color: 'text.primary',
                mt: 4, // Margen superior para separar del encabezado principal
              }}
            >
              Our Story
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ lineHeight: 1.7 }}>
              Founded from a shared passion for efficiency and clarity, we noticed a common challenge: professionals struggled to concisely articulate the impact of their work. Traditional methods were often time-consuming and didn't always capture the true value delivered. Driven by the belief that "the best way to do it" involves smart tools, we embarked on a mission to create a cutting-edge results statement generator. Our journey has been one of innovation, user-focused design, and a relentless pursuit of quality to help you showcase your achievements effortlessly.
            </Typography>
          </Box>

          {/* Misión */}
          <Box>
            <Typography
              variant="h4"
              component="h2"
              sx={{
                fontWeight: 'bold',
                mb: 2,
                textAlign: 'center',
                color: 'text.primary',
              }}
            >
              Our Mission
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ lineHeight: 1.7 }}>
              To empower professionals and organizations by providing an intuitive and powerful platform for crafting compelling result statements. We aim to simplify the process of quantifying achievements and communicating impact, enabling our users to effectively highlight their contributions, secure opportunities, and drive success.
            </Typography>
          </Box>

          {/* Visión */}
          <Box>
            <Typography
              variant="h4"
              component="h2"
              sx={{
                fontWeight: 'bold',
                mb: 2,
                textAlign: 'center',
                color: 'text.primary',
              }}
            >
              Our Vision
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ lineHeight: 1.7 }}>
              To be the leading solution for results-oriented communication, recognized globally for transforming how achievements are documented and shared. We envision a future where every professional can clearly and confidently articulate their value, fostering a world of greater recognition, collaboration, and continuous improvement.
            </Typography>
          </Box>
        </Stack>
        {/* <StyledBox id="image" /> */}
      </Container>
    </Box>
  );
}