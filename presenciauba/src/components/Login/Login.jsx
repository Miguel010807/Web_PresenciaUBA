import { useState } from "react";
import "./Login.css";

function Login({ onLogin }) {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://10.56.2.14:5000/login", {
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

      if (onLogin) {
        onLogin(data.user);
      }
    } catch (err) {
      console.error(err);
      setError("Credenciales invalidas.");
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
        {error && <p className="error">{error}</p>}
      </form>
      <footer className="footer-copy">
        © derechos reservados por la ETEC UBA
      </footer>
    </div>
  );
}

export default Login;
