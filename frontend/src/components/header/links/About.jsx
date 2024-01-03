import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { Button } from "@mui/material";

const AboutLink = () => (
    <Button 
        component={RouterLink} 
        to="/about" 
        style={{ color: '#192b3e', marginRight: '20px' }}
    >
        About
    </Button>
);
  
export default AboutLink;