import React from "react";
import { Box, Toolbar } from "@mui/material";
import Header from '../Header/Header';
import HomeLink from "../Header/Links/Home";
import LoginLink from "../Header/Links/Login";
import PricingLink from "../Header/Links/Pricing";
import BlogLink from "../Header/Links/Blog";
import AboutLink from "../Header/Links/About";

const LandingLayout = ({ children }) => {
    const navLinks = [
        <HomeLink key="home" />,
        <LoginLink key="login" />,
        <PricingLink key="pricing" />,
        <BlogLink key="blog" />,
        <AboutLink key="about" />
    ];

    return (
        <Box sx={{ display: 'flex' }}>
            <Header navLinks={navLinks} />
            <Box sx={{ flexGrow: 1 }}>
                <Toolbar />
                {children}
            </Box>
        </Box>
    );
};

export default LandingLayout;