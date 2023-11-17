import React from "react";
import { Box, Container, Typography, useTheme, useMediaQuery } from "@mui/material";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

const LandingPage = () => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const appBarHeight = '64px'; // Adjust this based on the AppBar content

    return (
        <Container maxWidth="lg" disableGutters={isMobile}>
            <Box
                component="main"
                sx={{ 
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center', // Center vertically
                    alignItems: 'center', // Center horizontally
                    textAlign: 'center',
                    height: `calc(100vh - ${appBarHeight})`, // Adjust for AppBar height
                }}
            >
                <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '80vh' }}>
                    <Typography variant="h6" color="text.secondary" gutterBottom>
                        DATA ANALYTICS REDEFINED: WHERE INTELLIGENCE MEETS INSIGHT.
                    </Typography>
                    <Typography variant="h3" component="h1" color={'#192B3E'}>
                        DocShow AI
                    </Typography>
                </Box>
                <Box sx={{ position: 'absolute', bottom: 20 }}>
                    <KeyboardArrowDownIcon fontSize="large" />
                </Box>
            </Box>
        </Container>
    );
};

export default LandingPage;
