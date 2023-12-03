// src/components/auth/Logout.js
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { useAuth } from '../contexts/AuthContext';

function Logout() {
  const navigate = useNavigate();
  const { updateAuth, isAuthenticated } = useAuth();

  useEffect(() => {
    // Clear the authentication cookie
    Cookies.remove('access_token');

    // Update authentication state
    updateAuth(false);

    // Redirect to the login page
    navigate('/');
  }, [navigate, updateAuth]);

  console.log(isAuthenticated)

  // Optionally, you can render a message or a spinner here
  return <div>Logging out...</div>;
}

export default Logout;
