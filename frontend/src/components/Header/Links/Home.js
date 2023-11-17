import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { Button } from "@mui/material";

const HomeLink = () => (
    <Button 
        component={RouterLink} 
        to="/" 
        style={{ color: '#192b3e', marginRight: '20px' }}
    >
        Home
    </Button>
);
  
export default HomeLink;