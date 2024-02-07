import React from "react";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Header from "../header/Header";
import Navigation from "../navigation/Navigation";
import BlogLink from "../header/links/Blog";
import AboutLink from "../header/links/About";
import LogoutLink from "../header/links/Logout";

const AppLayout = ({ children }) => {
  const navLinks = [
    <BlogLink key="blog" />,
    <AboutLink key="about" />,
    <LogoutLink key="logout" />,
  ];
  return (
    <Box sx={{ display: "flex" }}>
      <Header navLinks={navLinks} />
      <Navigation />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 6,
          marginTop: "10px",
          marginTop: "10px",
          maxWidth: "100vw", // Ensures the main content does not exceed the viewport width
          overflowX: "hidden",
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default AppLayout;
