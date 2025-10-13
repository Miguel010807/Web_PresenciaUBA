import React, { useState, useEffect } from "react";
import axios from "axios";

function Dashboard({ usuario, onLogout }) {
  const [mantenimiento, setMantenimiento] = useState(false);

  // Verifica si el sistema está en mantenimiento
  useEffect(() => {
    const checkMantenimiento = async () => {
      try {
        const response = await axios.post("http://localhost:5000/mantenimiento");
        setMantenimiento(false); // Resetear cuando el mantenimiento cambie
      } catch (error) {
        if (error.response && error.response.status === 503) {
          setMantenimiento(true); // El sistema está en mantenimiento
        }
      }
    };
    
    checkMantenimiento();
  }, []);

  if (mantenimiento) {
    return (
      <div className="maintenance-message">
        <h2>El sistema está en mantenimiento. Intente más tarde.</h2>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <h1>
        Bienvenido {usuario.nombre || usuario.correo_institucional}
      </h1>
      <button onClick={onLogout}>Cerrar sesión</button>
    </div>
  );
}

export default Dashboard;
