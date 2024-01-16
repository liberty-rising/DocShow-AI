import React, { useState } from "react";
import { Box, Button, TextField, Typography } from "@mui/material";
import Alert from "@mui/material/Alert";
import axios from "axios";
import validator from "validator";
import { API_URL } from "../../utils/constants";

function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Validate email
    if (!validator.isEmail(email)) {
      setErrorMessage("Please enter a valid email address.");
      return;
    }

    // Send request to backend server
    try {
      await axios.post(`${API_URL}users/forgot-password/`, { email });
      alert("Password reset email sent!");
    } catch (error) {
      setErrorMessage("Error sending password reset email. Please try again.");
    }
  };

  return (
    <Box
      sx={{
        marginTop: 8,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <Typography component="h1" variant="h5">
        Forgot Password
      </Typography>
      <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          id="email"
          label="Email Address"
          name="email"
          autoComplete="email"
          autoFocus
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
        >
          Reset Password
        </Button>
      </Box>
      {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
    </Box>
  );
}

export default ForgotPasswordPage;
