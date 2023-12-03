import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

function RequireAuth({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  console.log(`loading ${isLoading}`)

  if (isLoading) {
    return <div>Loading...</div>; // Or your preferred loading indicator/component
  }

  console.log(`isAuthenticated ${isAuthenticated}`)

  if (!isAuthenticated) {
    // Redirect to the login page if not authenticated
    return <Navigate to="/login" />;
  }

  return children;
}

export default RequireAuth