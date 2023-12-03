// src/contexts/AuthContext.js
import React, { createContext, useContext, useEffect, useState } from 'react';
import { API_URL } from '../utils/constants';

//Contexts in React are used for passing data deeply through the component tree without having to pass props down manually at every level
export const AuthContext = createContext();

// Custom hook for using our AuthContext. This makes it easier to access our authentication state and functions from any component in our app
export const useAuth = () => useContext(AuthContext);

// Component that provides authentication state to its children. 
// This component will wrap our app so that any child component can access the authentication state
export const AuthProvider = ({ children }) => {
  // State for keeping track of whether the user is authenticated. 
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true); // Add a loading state

  useEffect(() => {
    const verifyToken = async () => {
      try {
        // Update based on the response message
        if (response.data.message === "User is authenticated") {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        setIsAuthenticated(false);
        console.error('Token verification failed', error);
      }
      setIsLoading(false);
    };

    verifyToken();
  }, []);

  // Function for updating the authenticated state. 
  // This is used to change the authentication status (logged in or logged out) from anywhere in the app
  const updateAuth = (newAuthState) => {
    setIsAuthenticated(newAuthState);
  };

  // The Provider component from our created context is used here. 
  // It makes the `isAuthenticated` state and `updateAuth` function available to any descendants of this component
  return (
    <AuthContext.Provider value={{ isAuthenticated, updateAuth, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};
