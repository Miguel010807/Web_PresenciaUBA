import "../Dashboard/Dashboard.css";
import logo from "../../assets/images.jpeg";

function Dashboard({ usuario, onLogout }) {
  return (
    <div className="dashboard-container">
      <img src={logo} alt="UBA Técnica" className="dashboard-logo" />

      <div className="dashboard-content">
        <h1>
          Bienvenido{" "}
          {usuario.nombre
            ? usuario.nombre
            : usuario.correo_institucional || usuario.correo}
        </h1>
        <p>Has iniciado sesión correctamente</p>

        <button onClick={onLogout} className="logout-button">
          Cerrar sesión
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
