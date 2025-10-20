import React from "react";

function DashboardDocente({ usuario, onLogout }) {
  return (
    <div className="dashboard-container">
      <h1>Bienvenido Docente {usuario.nombre}</h1>
      <p>Rol: {usuario.rol}</p>
      <button onClick={onLogout}>Cerrar sesión</button>
    </div>
  );
}

export default DashboardDocente;
