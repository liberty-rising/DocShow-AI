import axios from "axios";
import { API_URL } from "../utils/constants";
import { navigate } from "../hooks/useNavigation";

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Check if the error is due to token expiration and the request is not for the refresh-token endpoint
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.includes("refresh-token/") && // Check if the failed request is not for the refresh-token endpoint
      !originalRequest.url.includes("token/") && // Exclude the login endpoint
      !originalRequest.url.includes("register/") && // Exclude the register endpoint
      !originalRequest.url.includes("forgot-password/") && // Exclude the forgot-password endpoint
      !originalRequest.url.includes("users/is-email-verified/") && // Exclude the is-email-verified endpoint
      !originalRequest.url.includes("users/verify-email/") && // Exclude the verify-email endpoint
      !originalRequest.url.includes("users/send-verification-email/")
    ) {
      // Exclude the send-verification-email endpoint
      originalRequest._retry = true;
      try {
        // Attempt to refresh the token
        console.log("Attempting token refresh");
        await axios.post(`${API_URL}refresh-token/`);
        // The browser will automatically include the updated cookies
        window.location.reload(); // Reload the page to use the new tokens
        return axios(originalRequest);
      } catch (refreshError) {
        if (window.location.pathname !== "/") {
          navigate("/login"); // Redirect to login
        }
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  },
);
