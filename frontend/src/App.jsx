import { React } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./api/axiosInterceptor";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import AppLayout from "./components/layouts/AppLayout";
import LandingLayout from "./components/layouts/LandingLayout";
import RequireAuth from "./components/auth/RequireAuth";
import RequireSysAdminAuth from "./components/auth/RequireSysAdminAuth";
import AboutPage from "./pages/about/AboutPage";
import AdminPage from "./pages/admin/AdminPage";
import AnalyticsPage from "./pages/analytics/AnalyticsPage";
import BlogPage from "./pages/blog/BlogPage";
import ChangePasswordPage from "./pages/change-password/ChangePasswordPage";
import CreateChartPage from "./pages/charts/CreateChartPage";
import CreateDashboardPage from "./pages/dashboards/CreateDashboard";
import CreateDataProfile from "./pages/data-profiling/CreateDataProfile";
import DashboardMenuPage from "./pages/dashboards/DashboardsMenuPage";
import Dashboard from "./pages/dashboards/Dashboard";
import DataProfilingPage from "./pages/data-profiling/DataProfilingPage";
import ForgotPasswordPage from "./pages/forgot-password/ForgotPasswordPage";
import LandingPage from "./pages/landing/LandingPage";
import LoginPage from "./pages/login/LoginPage";
import PricingPage from "./pages/pricing/PricingPage";
import RegisterPage from "./pages/register/RegisterPage";
import ResetPasswordPage from "./pages/reset-password/ResetPasswordPage";
import SpecificDataProfilePage from "./pages/data-profiling/SpecificDataProfilePage";
import UploadPage from "./pages/upload/UploadPage";
import UserPage from "./pages/user/UserPage";
import VerifyEmailPage from "./pages/verify-email/VerifyEmailPage";
import Logout from "./pages/logout/LogoutPage";

function AppWrapper() {
  return (
    <AuthProvider>
      <Router>
        <App />
      </Router>
    </AuthProvider>
  );
}

function App() {
  const { isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>; // Or any other loading indicator
  }

  return (
    <Routes>
      <Route
        path="/"
        element={
          <LandingLayout>
            <LandingPage />
          </LandingLayout>
        }
      />
      <Route
        path="/login"
        element={
          <LandingLayout>
            <LoginPage />
          </LandingLayout>
        }
      />
      <Route
        path="/change-password"
        element={
          <RequireAuth>
            <LandingLayout>
              <ChangePasswordPage />
            </LandingLayout>
          </RequireAuth>
        }
      />
      <Route
        path="/reset-password"
        element={
          <LandingLayout>
            <ResetPasswordPage />
          </LandingLayout>
        }
      />
      <Route
        path="/forgot-password"
        element={
          <LandingLayout>
            <ForgotPasswordPage />
          </LandingLayout>
        }
      />
      <Route
        path="/verify-email"
        element={
          <LandingLayout>
            <VerifyEmailPage />
          </LandingLayout>
        }
      />
      <Route
        path="/register"
        element={
          <LandingLayout>
            <RegisterPage />
          </LandingLayout>
        }
      />
      <Route
        path="/pricing"
        element={
          <LandingLayout>
            <PricingPage />
          </LandingLayout>
        }
      />
      <Route
        path="/blog"
        element={
          <LandingLayout>
            <BlogPage />
          </LandingLayout>
        }
      />
      <Route
        path="/about"
        element={
          <LandingLayout>
            <AboutPage />
          </LandingLayout>
        }
      />
      <Route
        path="/dashboards"
        element={
          <RequireAuth>
            <AppLayout>
              <DashboardMenuPage />
            </AppLayout>
          </RequireAuth>
        }
      />
      <Route
        path="/dashboards/create"
        element={
          <RequireAuth>
            <AppLayout>
              <CreateDashboardPage />
            </AppLayout>
          </RequireAuth>
        }
      />
      <Route
        path="/dashboards/:dashboardId"
        element={
          <RequireAuth>
            <AppLayout>
              <Dashboard />
            </AppLayout>
          </RequireAuth>
        }
      />
      <Route
        path="/dashboards/:dashboardId/charts/create"
        element={
          <RequireAuth>
            <AppLayout>
              <CreateChartPage />
            </AppLayout>
          </RequireAuth>
        }
      />
      <Route
        path="/upload"
        element={
          <RequireAuth>
            <AppLayout>
              <UploadPage />
            </AppLayout>
          </RequireAuth>
        }
      />
      <Route
        path="/analytics"
        element={
          <RequireAuth>
            <AppLayout>
              <AnalyticsPage />
            </AppLayout>
          </RequireAuth>
        }
      />
      <Route
        path="/user"
        element={
          <RequireAuth>
            <AppLayout>
              <UserPage />
            </AppLayout>
          </RequireAuth>
        }
      />
      <Route
        path="/admin"
        element={
          <RequireSysAdminAuth>
            <RequireAuth>
              <AppLayout>
                <AdminPage />
              </AppLayout>
            </RequireAuth>
          </RequireSysAdminAuth>
        }
      />
      <Route
        path="/logout"
        element={
          <RequireAuth>
            <Logout />
          </RequireAuth>
        }
      />
    </Routes>
  );
}

export default AppWrapper;
