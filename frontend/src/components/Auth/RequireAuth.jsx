import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

function RequireAuth({ children }) {
  const { isAuthenticated, isLoading, isEmailVerified } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>; // Or your preferred loading indicator/component
  }

  if (!isAuthenticated) {
    // Redirect to the login page if not authenticated
    return <Navigate to="/login" />;
  }

  if (!isEmailVerified) {
    // Redirect to the verify-email page if email is not verified
    return <Navigate to="/verify-email" />;
  }

  return children;
}

export default RequireAuth