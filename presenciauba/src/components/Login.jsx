import { useState } from "react";

function Login({ onLogin }) {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ correo, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Error en el login");
        return;
      }

      // Guardamos el usuario en localStorage
      localStorage.setItem("usuario", JSON.stringify(data.usuarios));

      // Avisamos al componente padre
      onLogin(data.usuarios);
    } catch (err) {
      console.log(err);
      setError("No se pudo conectar con el backend.");
    }
  };

  return (
    <div className="login-container">
      <h2>Presencia UBA</h2>
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