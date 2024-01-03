import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { Button } from "@mui/material";

const PricingLink = () => (
    <Button 
        component={RouterLink} 
        to="/pricing" 
        style={{ color: '#192b3e', marginRight: '20px' }}
    >
        Pricing
    </Button>
);
  
export default PricingLink;