import React from "react";
import { Box, Toolbar } from "@mui/material";
import Header from "../header/Header";
import HomeLink from "../header/links/Home";
import LoginLink from "../header/links/Login";
import PricingLink from "../header/links/Pricing";
import BlogLink from "../header/links/Blog";
import AboutLink from "../header/links/About";

const LandingLayout = ({ children }) => {
  const navLinks = [
    <HomeLink key="home" />,
    <LoginLink key="login" />,
    <PricingLink key="pricing" />,
    <BlogLink key="blog" />,
    <AboutLink key="about" />,
  ];

  return (
    <Box sx={{ display: "flex" }}>
      <Header navLinks={navLinks} />
      <Box sx={{ flexGrow: 1 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default LandingLayout;
