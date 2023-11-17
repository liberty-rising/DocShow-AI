import { React } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import AppLayout from './components/layouts/AppLayout';
import LandingLayout from './components/layouts/LandingLayout';
import AboutPage from './pages/About';
import AdminPage from './pages/Admin/Admin';
import AIAssistantPage from './pages/AIAssistant';
// import AnalyticsPage from './pages/Analytics/Analytics';
import BlogPage from './pages/Blog';
import DashboardPage from './pages/Dashboard';
import LandingPage from './pages/Landing';
import LoginPage from './pages/Login';
import PricingPage from './pages/Pricing';
import RegisterPage from './pages/Register';
import UploadPage from './pages/Upload/Upload';
import UserPage from './pages/User';
import Logout from './pages/Logout';

function AppWrapper() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  )
}

function App() {
  const { isAuthenticated, isLoading } = useAuth(); // Use the `isAuthenticated` from the context
  
  if (isLoading) {
    return <div>Loading...</div>; // Or any other loading indicator
  }

  return (
    <Router>
      <Routes>
        <Route 
          path="/" 
          element={isAuthenticated ? <AppLayout><DashboardPage /></AppLayout> : <LandingLayout><LandingPage /></LandingLayout>} 
        />
        <Route 
          path="/login" 
          element={<LandingLayout>
                <LoginPage />
            </LandingLayout>
          } 
        />
        <Route path="/register" element={<LandingLayout><RegisterPage /></LandingLayout>} />
        <Route path="/pricing" element={<LandingLayout><PricingPage /></LandingLayout>} />
        <Route path="/blog" element={<LandingLayout><BlogPage /></LandingLayout>} />
        <Route path="/about" element={<LandingLayout><AboutPage /></LandingLayout>} />
        <Route path="/upload" element={<AppLayout><UploadPage /></AppLayout>} />
        {/* <Route path="/analytics" element={<AppLayout><AnalyticsPage /></AppLayout>} /> */}
        <Route path="/ai-assistant" element={<AppLayout><AIAssistantPage /></AppLayout>} />
        <Route path="/user" element={<AppLayout><UserPage /></AppLayout>} />
        <Route path="/admin" element={<AppLayout><AdminPage /></AppLayout>} />
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </Router>
  );
}

export default AppWrapper;
