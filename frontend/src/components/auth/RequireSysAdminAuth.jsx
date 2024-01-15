import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

function RequireSysAdminAuth({ children }) {
  const { isAuthenticated, isLoading, userRole } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>; // Or your preferred loading indicator/component
  }

  if (!isAuthenticated || userRole !== 'system_admin') {
    // Redirect to the login page if not authenticated or not a system admin
    return <Navigate to="/login" />;
  }

  return children;
}

export default RequireSysAdminAuth;