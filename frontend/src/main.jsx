import React from "react";
import ReactDOM from "react-dom/client";
import AppWrapper from "./App.jsx";

// React.StrictMode is a wrapper component that checks for potential problems in the app during development.
// It intentionally double-invokes certain methods (including render methods) to help detect side-effects.
// This double-invocation only happens in development mode, not in production.
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AppWrapper />
  </React.StrictMode>,
);
