import React from "react";
import { Routes, Route } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";

function App() {
  return (
    <Routes>
      {/* Route for the Login Page */}
      <Route path="/login" element={<LoginPanel />} />

      {/* Route for the Register Page */}
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}

export default App;

