import { Box, FormControl, TextField, Typography, FormLabel, CssBaseline } from "@mui/material";
import AppTheme from "../../theme/AppTheme";
import AppAppBar from "../layout/aboutUs/AppBar";
import Content from "../layout/aboutUs/Content";
import FAQ from "../layout/aboutUs/FAQ";
import Footer from "../layout/Footer";

export default function AboutUs(props) {

    return(
        <AppTheme>
            <CssBaseline enableColorScheme/>
            <AppAppBar />
            <Content />
            <FAQ />
            <Footer />
        </AppTheme>
    );
}
