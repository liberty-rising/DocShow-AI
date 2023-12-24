import { React } from 'react';
import {
  BrowserRouter as Router,
  Navigate,
  Routes,
  Route
} from 'react-router-dom';
import './api/axiosInterceptor'
import { NavigationProvider } from './hooks/useNavigation';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import AppLayout from './components/layouts/AppLayout';
import LandingLayout from './components/layouts/LandingLayout';
import RequireAuth from './components/auth/RequireAuth';
import AboutPage from './pages/About';
import AdminPage from './pages/admin/Admin';
import AnalyticsPage from './pages/analytics/AnalyticsPage';
import BlogPage from './pages/Blog';
import CreateChartPage from './pages/charts/CreateChart';
import CreateDashboardPage from './pages/dashboards/CreateDashboard';
import DashboardMenuPage from './pages/dashboards/DashboardsMenuPage';
import Dashboard from './pages/dashboards/Dashboard';
import DataProfilingPage from './pages/data-profiling/DataProfiling';
import CreateDataProfile from './pages/data-profiling/CreateDataProfile';
import SpecificDataProfilePage from './pages/data-profiling/SpecificDataProfilePage';
import LandingPage from './pages/Landing'; 
import LoginPage from './pages/Login';
import PricingPage from './pages/Pricing';
import RegisterPage from './pages/Register';
import UploadPage from './pages/upload/Upload';
import UserPage from './pages/user/UserPage';
import Logout from './pages/Logout';

function AppWrapper() {
  return (
    <AuthProvider>
      <Router>
        <NavigationProvider>
          <App />
        </NavigationProvider>
      </Router>
    </AuthProvider>
  )
}

function App() {
  const { isAuthenticated, isLoading } = useAuth(); // Use the `isAuthenticated` from the context
  
  if (isLoading) {
    return <div>Loading...</div>; // Or any other loading indicator
  }

  return (
    <Routes>
      <Route
        path="/" 
        element={<LandingLayout><LandingPage /></LandingLayout>} 
      />
      <Route 
        path="/login" 
        element={isAuthenticated ? <Navigate to ="/dashboards" /> : 
          <LandingLayout><LoginPage /></LandingLayout>} 
      />
      <Route path="/register" element={<LandingLayout><RegisterPage /></LandingLayout>} />
      <Route path="/pricing" element={<LandingLayout><PricingPage /></LandingLayout>} />
      <Route path="/blog" element={<LandingLayout><BlogPage /></LandingLayout>} />
      <Route path="/about" element={<LandingLayout><AboutPage /></LandingLayout>} />
      <Route path="/dashboards" element={<RequireAuth><AppLayout><DashboardMenuPage /></AppLayout></RequireAuth>} />
      <Route path="/dashboards/create" element={<RequireAuth><AppLayout><CreateDashboardPage /></AppLayout></RequireAuth>} />
      <Route path="/dashboards/:dashboardId" element={<RequireAuth><AppLayout><Dashboard /></AppLayout></RequireAuth>} />
      <Route path="/dashboards/:dashboardId/charts/create" element={<RequireAuth><AppLayout><CreateChartPage /></AppLayout></RequireAuth>} />
      <Route path="/upload" element={<RequireAuth><AppLayout><UploadPage /></AppLayout></RequireAuth>} />
      <Route path="/analytics" element={<RequireAuth><AppLayout><AnalyticsPage /></AppLayout></RequireAuth>} />
      <Route path="/data-profiling" element={<RequireAuth><AppLayout><DataProfilingPage /></AppLayout></RequireAuth>} />
      <Route path="/data-profiling/:dataProfileId" element={<RequireAuth><AppLayout><SpecificDataProfilePage /></AppLayout></RequireAuth>} />
      <Route path="/data-profiling/create" element={<RequireAuth><AppLayout><CreateDataProfile /></AppLayout></RequireAuth>} />
      <Route path="/user" element={<RequireAuth><AppLayout><UserPage /></AppLayout></RequireAuth>} />
      <Route path="/admin" element={<RequireAuth><AppLayout><AdminPage /></AppLayout></RequireAuth>} />
      <Route path="/logout" element={<RequireAuth><Logout /></RequireAuth>} />
    </Routes>
  );
}

export default AppWrapper;
