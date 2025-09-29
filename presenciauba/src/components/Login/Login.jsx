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

      // Guardamos el token en localStorage
      localStorage.setItem("token", data.token || "");

      // Guardamos también el usuario (sin contraseña si querés)
      localStorage.setItem("usuario", JSON.stringify(data.user));

      // Avisamos al componente padre
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
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Correo institucional"
          value={correo}
          onChange={(e) => setCorreo(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Iniciar sesión</button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}

export default Login;
