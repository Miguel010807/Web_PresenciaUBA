import React from "react";

function DashboardEstudiante({ usuario, onLogout }) {
  return (
    <div className="dashboard-container">
      <h1>
        Bienvenido Estudiante {usuario.nombre || usuario.correo_institucional}
      </h1>
      <p>Rol: {usuario.rol}</p>
      <button onClick={onLogout}>Cerrar sesión</button>
    </div>
  );
}

export default DashboardEstudiante;
