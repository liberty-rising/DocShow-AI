import React from "react";
import { Link as RouterLink } from "react-router-dom";
import Button from '@mui/material/Button';


const LoginLink = () => (
    <Button 
        component={RouterLink} 
        to="/login" 
        style={{ color: '#192b3e', marginRight: '20px' }}
    >
        Login
    </Button>
);
  
export default LoginLink;