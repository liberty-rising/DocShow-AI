import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import { Link } from 'react-router-dom';

const Header = ({ navLinks }) => {
    return (
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, backgroundColor: 'white' }}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Link to="/" style={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}>
            <img src={"/logo-header.png"} alt="logo" style={{ marginRight: '10px', maxHeight: '50px' }} />
            <Typography variant="h6" noWrap component="div" style={{ color: '#192b3e' }}>
              DocShow AI
            </Typography>
          </Link>
          <Box sx={{ display: 'flex' }}>
            {navLinks}
          </Box>
        </Toolbar>
      </AppBar>
    );
};
  
export default Header;
