import { Box, FormControl, TextField, Typography, FormLabel, CssBaseline } from "@mui/material";
import AppTheme from "../../theme/AppTheme";
import AppAppBar from "../layout/aboutUs/AppBar";
import Content from "../layout/aboutUs/Content";
import FAQ from "../layout/aboutUs/FAQ";
import Footer from "../layout/Footer";
import { useEffect, useState } from "react";

function FinancialNewsTicker() {
  const [headlines, setHeadlines] = useState([]);

  useEffect(() => {
    async function fetchNews() {
      try {
        const res = await fetch(
            "https://newsapi.org/v2/everything?domains=wsj.com&apiKey=8783ccc2db0f4e4eb6f27389ad4b3273"
        );
        const data = await res.json();
        setHeadlines(data.articles ? data.articles.map((a) => a.title) : []);
      } catch (err) {
        console.error(err);
        setHeadlines([
          "No se pudieron cargar las noticias financieras en este momento.",
        ]);
      }
    }
    fetchNews();
  }, []);

  const tickerContent = [...headlines, ...headlines];

  return (
    <Box
      sx={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        overflow: "hidden",
        bgcolor: "#0d47a1",
        color: "common.white",
        zIndex: (theme) => theme.zIndex.appBar + 1,
        py: 1,
      }}
    >
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

export default function AboutUs(props) {

    return(
        <AppTheme>
            <CssBaseline enableColorScheme/>
            <FinancialNewsTicker />

            <AppAppBar sx={{ mt: 10 }} />
            <Content />
            <FAQ />
            <Footer />

        </AppTheme>
    );
}
