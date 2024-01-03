import React from "react";
import { Link as RouterLink } from "react-router-dom";
import Button from '@mui/material/Button';


const LogoutLink = () => (
    <Button 
        component={RouterLink} 
        to="/logout" 
        style={{ color: '#192b3e', marginRight: '20px' }}
    >
        Logout
    </Button>
);
  
export default LogoutLink;