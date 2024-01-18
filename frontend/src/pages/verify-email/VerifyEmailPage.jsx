import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  Container,
  Snackbar,
  Typography,
} from "@mui/material";
import { useAuth } from "../../contexts/AuthContext";
import { API_URL } from "../../utils/constants";
import axios from "axios";
import { set } from "date-fns";

const VerifyEmailPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [userResponse, setUserResponse] = useState(null);
  const [token, setToken] = useState(null);
  const { updateAuth, updateEmailVerification, loginProcessCompleted } =
    useAuth();
  const [openAlert, setOpenAlert] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const token = params.get("token");
    setToken(token);
  }, [location]);

  useEffect(() => {
    if (!token) {
      axios
        .get(`${API_URL}users/me/`)
        .then((response) => {
          if (response.data) {
            setUserResponse(response.data);
          } else {
            // If no user data is returned, navigate to the login page
            navigate("/login");
          }
        })
        .catch((error) => {
          // If an error occurs, navigate to the login page
          navigate("/login");
        });
    }
  }, [token]);

  useEffect(() => {
    if (token) {
      console.log("token", token);
      axios
        .put(`${API_URL}users/verify-email/`, { token })
        .then((response) => {
          // Handle successful verification
          updateEmailVerification(true);

          axios
            .get(`${API_URL}verify-token/`)
            .then((response) => {
              // Handle successful token verification
              updateAuth(true);
              console.log("Token verified successfully");
              navigate("/dashboards");
            })
            .catch((error) => {
              // Handle failed token verification
              console.log("Failed to verify token");
              navigate("/login");
            });
        })
        .catch((error) => {
          // Handle failed verification
          navigate("/login");
        });
    }
  }, [token, navigate, updateEmailVerification]);

  const handleResendEmail = async (event) => {
    event.preventDefault();
    axios
      .post(`${API_URL}users/send-verification-email/`, {
        email: userResponse.email,
      })
      .then((response) => {
        // Handle successful email resend
        console.log("Verification email sent successfully");
        setOpenAlert(true);
      })
      .catch((error) => {
        // Handle failed email resend
        console.log("Failed to send verification email");
      });
  };

  const handleCloseAlert = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }
    setOpenAlert(false);
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography variant="h4" align="center" gutterBottom>
          Verify Your Email
        </Typography>
        <Typography variant="body1" align="center" gutterBottom>
          We've sent a verification link to your email address. Please check
          your inbox and click the link to verify your email.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          fullWidth
          onClick={handleResendEmail}
        >
          Resend Verification Email
        </Button>
        <Snackbar
          open={openAlert}
          autoHideDuration={6000}
          onClose={handleCloseAlert}
        >
          <Alert
            onClose={handleCloseAlert}
            severity="success"
            sx={{ width: "100%" }}
          >
            Verification email has been resent!
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
};

export default VerifyEmailPage;
