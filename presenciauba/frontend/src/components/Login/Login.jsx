import FacebookLogin from "./FacebookLogin"; // ajustá la ruta si está en otra carpeta
import { useState } from "react";
import "./Login.css";

function Login({ onLogin }) {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [nuevaPassword, setNuevaPassword] = useState("");
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [mostrarCambio, setMostrarCambio] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://10.56.2.56:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correo, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Error en el login");
        return;
      }

      localStorage.setItem("token", data.token || "");
      localStorage.setItem("usuario", JSON.stringify(data.user));

      if (onLogin) onLogin(data.user);

      setMostrarCambio(true); // Mostrar el formulario de cambio
      setMensaje("Inicio de sesión exitoso");
      setError("");
    } catch (err) {
      console.error(err);
      setError("Credenciales inválidas.");
    }
  };

  const handleCambioPassword = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");
    if (!token) {
      setError("No hay token de sesión");
      return;
    }

    try {
      const res = await fetch("http://10.56.2.56:5000/cambiar_contraseña", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ nueva_contraseña: nuevaPassword }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "No se pudo cambiar la contraseña");
        return;
      }

      setMensaje(data.mensaje || "Contraseña actualizada correctamente");
      setError("");
      setNuevaPassword("");
    } catch (err) {
      console.error(err);
      setError("Error en la conexión");
    }
  };

  return (
    <div className="login-container">
      <h2 className="login-titulo">Presencia UBA</h2>

      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label htmlFor="correo">Correo institucional:</label>
          <input
            id="correo"
            type="email"
            placeholder="ejemplo@etec.uba.ar"
            value={correo}
            onChange={(e) => setCorreo(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Contraseña:</label>
          <input
            id="password"
            type="password"
            placeholder="ingrese su contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Iniciar sesión</button>
{/* --- Agregamos login con Facebook --- */}
<div className="divider">
  <hr />
  <span>o</span>
  <hr />
</div>

<FacebookLogin
  onLoginSuccess={(data) => {
    console.log("Inicio de sesión con Facebook exitoso:", data);

    // Guardamos el token que viene desde Flask (si lo envía)
    localStorage.setItem("token", data.access_token || "");

    // También podrías simular un usuario con rol
    localStorage.setItem(
      "usuario",
      JSON.stringify({ nombre: "Usuario Facebook", rol: data.role })
    );

    if (onLogin) onLogin({ nombre: "Usuario Facebook", rol: data.role });
  }}
  sizeClass="facebook-btn"
/>

        {error && <p className="error">{error}</p>}
        {mensaje && <p className="mensaje">{mensaje}</p>}
      </form>

      {mostrarCambio && (
        <form onSubmit={handleCambioPassword} className="login-form">
          <h3>Cambiar contraseña</h3>
          <div className="form-group">
            <label htmlFor="nuevaPassword">Nueva contraseña:</label>
            <input
              id="nuevaPassword"
              type="password"
              placeholder="Ingrese la nueva contraseña"
              value={nuevaPassword}
              onChange={(e) => setNuevaPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Guardar nueva contraseña</button>
        </form>
      )}

      <footer className="footer-copy">
        © derechos reservados por la ETEC UBA
      </footer>
    </div>
  );
}

export default Login;
