import axios from 'axios';
import { API_URL } from '../utils/constants';
import { navigate } from '../hooks/useNavigation';

axios.interceptors.response.use(response => response, async (error) => {
    const originalRequest = error.config;

    // Check if the error is due to token expiration
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        try {
            // Attempt to refresh the token
            console.log("Attempting token refresh")
            await axios.post(`${API_URL}/refresh-token/`);
            // The browser will automatically include the updated cookies
            return axios(originalRequest); // Retry the original request
        } catch (refreshError) {
            navigate('/login'); // Redirect to login
            return Promise.reject(refreshError);
        }
    }

    return Promise.reject(error);
});
