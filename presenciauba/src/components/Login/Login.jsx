import { useState } from "react";
import "./Login.css";

function Login({ onLogin }) {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://10.56.2.47:5000/login", {
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
      setError("No se pudo conectar con el backend.");
    }
  };

  return (
    <div className="login-container">
      <h2 className="login-titulo">Presencia UBA</h2>
      <form onSubmit={handleSubmit} className="login-form">
        {" "}
        {/* Añadimos una clase al formulario para el CSS */}
        {/* Campo de Correo Institucional */}
        <div className="form-group">
          {" "}
          {/* Envolvemos label e input */}
          <label htmlFor="correo">Correo institucional:</label>
          <input
            id="correo" // Añadimos un id para relacionarlo con la label
            type="email"
            placeholder="ejemplo@etec.uba.ar" // Cambiamos el placeholder para que no repita la label
            value={correo}
            onChange={(e) => setCorreo(e.target.value)}
            required
          />
        </div>
        {/* Campo de Contraseña */}
        <div className="form-group">
          {" "}
          {/* Envolvemos label e input */}
          <label htmlFor="password">Contraseña:</label>
          <input
            id="password" // Añadi un id para relacionarlo con la label
            type="password"
            placeholder="ingrese su contraseña" // Cambiamos el placeholder
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Iniciar sesión</button>
        {error && <p className="error">{error}</p>}
      </form>
      {/* Footer agregado */}
      <footer className="footer-copy">
        © derechos reservados por la ETEC UBA <br />
        Hecho por Thiago Gomez y Miguel Díaz
      </footer>
    </div>
  );
}

export default Login;
