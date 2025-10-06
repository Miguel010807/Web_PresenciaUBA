function Dashboard({ usuario, onLogout }) {
  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>
        Bienvenido{" "}
        {usuario.nombre
          ? usuario.nombre
          : usuario.correo_institucional || usuario.correo}
      </h1>
      <p>Has iniciado sesión correctamente 🎉</p>

      <button
        onClick={onLogout}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          borderRadius: "8px",
          backgroundColor: "#d9534f",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Cerrar sesión
      </button>
    </div>
  );
}

export default Dashboard;