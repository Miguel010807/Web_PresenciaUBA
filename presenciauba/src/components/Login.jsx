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
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correo, password }),
      });
      
      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Error en el login");
        return;
      }

      // Guardamos el token en localStorage
      localStorage.setItem("token", data.token);

      // Guardamos también el usuario (sin contraseña)
      localStorage.setItem("usuario", JSON.stringify(data.user));

      // Avisamos al componente padre
      onLogin(data.user);
    } catch (err) {
      console.log(err);
      setError("No se pudo conectar con el backend.");
    }
  };

  return (
    <div className="login-container">
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
