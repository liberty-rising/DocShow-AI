import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

function RequireAuth({ children }) {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    // Redirect to the login page if not authenticated
    return <Navigate to="/login" />;
  }

  return children;
}

export default RequireAuth