import * as React from 'react';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DateField } from '@mui/x-date-pickers/DateField';
import { styled, ThemeProvider } from '@mui/material/styles';
import AppTheme from '../../theme/AppTheme'
import { CssBaseline } from '@mui/material';

export default function BasicDateField() {
  return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DemoContainer components={['DateField']}>
            <DateField label="Basic date field" 
              sx={{
                backgroundColor: 'aliceblue',
              }}/>
          </DemoContainer>
        </LocalizationProvider>
  );
}
