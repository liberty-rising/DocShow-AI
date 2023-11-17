import React from 'react';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Header from '../Header/Header';
import Navigation from '../Navigation/Navigation';
import BlogLink from '../Header/Links/Blog';
import AboutLink from '../Header/Links/About';
import LogoutLink from '../Header/Links/Logout';

const AppLayout = ({ children }) => {
    const navLinks = [
        <BlogLink key="blog" />,
        <AboutLink key="about" />,
        <LogoutLink key="logout" />
    ]
    return (
        <Box sx={{ display: 'flex' }}>
            <Header navLinks={navLinks}/>
            <Navigation />
            <Box component="main" sx={{ flexGrow: 1, p: 3, marginTop: '64px' }}>
                <Toolbar />
                {children}
            </Box>
        </Box>
    );
};

export default AppLayout;
