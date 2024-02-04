import React, { useEffect } from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import "./api/axiosInterceptor";
import RequireAuth from "./components/auth/RequireAuth";
import RequireSysAdminAuth from "./components/auth/RequireSysAdminAuth";
import AppLayout from "./components/layouts/AppLayout";
import LandingLayout from "./components/layouts/LandingLayout";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import AboutPage from "./pages/about/AboutPage";
import AdminPage from "./pages/admin/AdminPage";
import AIAnalystPage from "./pages/ai-analyst/AIAnalystPage";
import BlogPage from "./pages/blog/BlogPage";
import ChangePasswordPage from "./pages/change-password/ChangePasswordPage";
import CreateChartPage from "./pages/charts/CreateChartPage";
import CreateDashboardPage from "./pages/dashboards/CreateDashboard";
import Dashboard from "./pages/dashboards/Dashboard";
import DashboardMenuPage from "./pages/dashboards/DashboardsMenuPage";
import ForgotPasswordPage from "./pages/forgot-password/ForgotPasswordPage";
import LandingPage from "./pages/landing/LandingPage";
import LoginPage from "./pages/login/LoginPage";
import Logout from "./pages/logout/LogoutPage";
import PricingPage from "./pages/pricing/PricingPage";
import RegisterPage from "./pages/register/RegisterPage";
import ResetPasswordPage from "./pages/reset-password/ResetPasswordPage";
import UploadPage from "./pages/upload/UploadPage";
import UserPage from "./pages/user/UserPage";
import VerifyEmailPage from "./pages/verify-email/VerifyEmailPage";
import ReportPage from "./pages/dashboards/ReportPage";
import { APP_ENV } from "./utils/constants";

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

  useEffect(() => {
    if (APP_ENV === "dev") {
      document.title = "DocShow AI - Dev";
    } else {
      document.title = "DocShow AI";
    }
  }, []);

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
        path="/dashboards/:report_id"
        element={
          <RequireAuth>
            <ReportPage />
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
        path="/ai-analyst"
        element={
          <RequireAuth>
            <AppLayout>
              <AIAnalystPage />
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
