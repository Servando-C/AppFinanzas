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
import { useTheme } from '@mui/material/styles';
import logo from '../../../assets/logo-ligh.svg?react';
import SvgIcon from '@mui/icons-material/Webhook';


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
          spacing={2}
          useFlexGap
          sx={{ alignItems: 'center', mt: 10, width: { xs: '100%', sm: '70%' } }}
        >
          {/* Nuestra Historia */}
          
            <Typography
            variant="h1"
            sx={{
              display: 'flex',
              flexDirection: { xs: 'column', sm: 'row' },
              alignItems: 'center',
              fontSize: 'clamp(2.5rem, 10vw, 3rem)',
            }}
          >
            About&nbsp;
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
               us
            </Typography>
          </Typography>
          <SvgIcon component={logo}
            inheritViewBox
            sx={{ width: 'auto', height: 100, alignSelf: 'center', mt: 4}}
            color='primary' />
          <Box>
            <Typography
              variant="h4" // O h2, h3 según tu jerarquía semántica
              component="h2"
              sx={{
                fontWeight: 'bold',
                mb: 2, // Margen inferior para separar del párrafo
                textAlign: 'center', // Título centrado
                color: 'text.primary',
                mt: 4, // Margen superior para separar del encabezado principal
                fontSize: 'clamp(1rem, 10vw, 2rem)',
              }}
            >
              Our Story
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ lineHeight: 1.7, fontSize: 'clamp(0.9rem, 2vw, 1rem)' }}>
              Founded in 2018 in Mexico City by a team of bankers and developers passionate about data, Snowflakes was born with the mission to crystallize companies' financial information. After launching its first analytics engine in the cloud in 2020, the firm connected more than 1 200 companies across Latin America in an ecosystem where financial statements are as clear as fresh snow.
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
                fontSize: 'clamp(1rem, 10vw, 2rem)',
              }}
            >
              Our Mission
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ lineHeight: 1.7, fontSize: 'clamp(0.9rem, 2vw, 1rem)' }}>
              Democratize access to clear, real-time, quality audited financial information, so that every company - regardless of size - can make informed decisions that drive responsible and sustainable growth.
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
                fontSize: 'clamp(1rem, 10vw, 2rem)',
              }}
            >
              Our Vision
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ lineHeight: 1.7, fontSize: 'clamp(0.9rem, 2vw, 1rem)' }}>
              To be the Latin American platform of reference where transparency and financial intelligence combine to foster resilient, prosperous and socially conscious organizations
            </Typography>
          </Box>
        </Stack>
      </Container>
    </Box>
  );
}