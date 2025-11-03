import { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./components/Login/Login";
import DashboardDocente from "./components/Dashboard/DashboardDocente";
import DashboardEstudiante from "./components/Dashboard/DashboardEstudiante";

function App() {
  const [usuario, setUsuario] = useState(
    JSON.parse(localStorage.getItem("usuario")) || null
  );

  const handleLogin = (user) => {
    setUsuario(user);
    localStorage.setItem("usuario", JSON.stringify(user));
  };

  const handleLogout = () => {
    localStorage.removeItem("usuario");
    localStorage.removeItem("token");
    setUsuario(null);
  };

  return (
    <Router>
      <Routes>
        {/* LOGIN */}
        <Route
          path="/"
          element={
            usuario ? (
              usuario.rol === "estudiante" ? (
                <Navigate to="/dashboard-estudiante" replace />
              ) : usuario.rol === "docente" ? (
                <Navigate to="/dashboard-docente" replace />
              ) : (
                <Navigate to="/" replace />
              )
            ) : (
              <Login onLogin={handleLogin} />
            )
          }
        />

        {/* DASHBOARD ESTUDIANTE */}
        <Route
          path="/dashboard-estudiante"
          element={
            usuario && usuario.rol === "estudiante" ? (
              <DashboardEstudiante usuario={usuario} onLogout={handleLogout} />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />

        {/* DASHBOARD DOCENTE */}
        <Route
          path="/dashboard-docente"
          element={
            usuario && usuario.rol === "docente" ? (
              <DashboardDocente usuario={usuario} onLogout={handleLogout} />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
