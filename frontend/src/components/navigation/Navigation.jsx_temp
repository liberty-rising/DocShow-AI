import React, { useState } from 'react';
import { Box, Divider, Drawer, IconButton, List, ListItemButton, ListItemIcon, ListItemText, Toolbar, Tooltip } from '@mui/material';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import DashboardIcon from '@mui/icons-material/Dashboard'
import UploadFileIcon from '@mui/icons-material/UploadFile';

import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import { useNavigate } from 'react-router-dom';

const Navigation = () => {
  const navigate = useNavigate();
  const [isDrawerOpen, setIsDrawerOpen] = useState(true); // State to manage drawer toggle
  const drawerWidth = isDrawerOpen ? 220 : 60; // 60px for collapsed width

  // Toggle drawer function
  const toggleDrawer = () => {
    setIsDrawerOpen(!isDrawerOpen);
  };

  const menuItems = [
    { text: 'Dashboards', icon: <DashboardIcon />, path: '/dashboards' },
    { text: 'Data Upload', icon: <UploadFileIcon />, path: '/upload' },
    { text: 'Data Analytics', icon: <AnalyticsIcon />, path: '/analytics' },
    { text: 'Data Profiling', icon: <AnalyticsIcon />, path: '/data-profiling' },
    { text: 'User Panel', icon: <AccountBoxIcon />, path: '/user' },
    { text: 'Admin Panel', icon: <AdminPanelSettingsIcon />, path: '/admin' },
    // { text: 'Logout', icon: <LogoutIcon />, path: '/logout' }
  ];

  return (
    <Box sx={{ display: 'flex' }}>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          height: '100vh',
          [`& .MuiDrawer-paper`]: { 
            width: drawerWidth, 
            boxSizing: 'border-box', 
            position: 'fixed', // This might still constrain the IconButton
            overflow: 'visible', // Set overflow to visible
            height: '100vh',
          },
        }}
      >
        <Toolbar />
        <Divider />
        <List sx={{ overflow: 'hidden' }}> {/* Adjust height based on Toolbar height */}
          {menuItems.map((item) => (
            isDrawerOpen ? // Only show Tooltip when drawer is closed
              <ListItemButton key={item.text} onClick={() => navigate(item.path)}>
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            :
              <Tooltip title={item.text} placement="right" key={item.text}>
                <ListItemButton onClick={() => navigate(item.path)}>
                  <ListItemIcon>{item.icon}</ListItemIcon>
                </ListItemButton>
              </Tooltip>
          ))}
        </List>
      </Drawer>
      <IconButton
        onClick={toggleDrawer}
        sx={{
          position: 'fixed',
          top: '50%', // Center vertically
          // right: isDrawerOpen ? '825px' : '60px', // You might need to adjust this value
          marginLeft: isDrawerOpen ? `${drawerWidth - 24}px` : '37px',
          transform: 'translateY(-50%)',
          zIndex: 1300, // Higher z-index to ensure visibility
          borderRadius: '30%', // Optional styling
          border: '1px solid', // Optional styling
          borderColor: 'divider', // Optional styling
          backgroundColor: 'background.paper', // Temporarily set a contrasting color
          width: 30, // Adjust size if needed
          height: 30, // Adjust size if needed
          '&:hover': {
            backgroundColor: '#f0f0f0',
          },
        }}
      >
        {isDrawerOpen ? <ChevronLeftIcon /> : <ChevronRightIcon />}
      </IconButton>
    </Box>
  );
};

export default Navigation;