import React, { useState } from "react";
import { login } from "../api";

export default function Login({ setUsuario }) {
  const [correo, setCorreo] = useState("");

  const handleLogin = async () => {
    try {
      const data = await login(correo);
      setUsuario(data.usuario);
    } catch (err) {
      alert("Error en login: " + err.response.data.error);
    }
  };

  return (
    <div>
      <h2>Presencia UBA - Login</h2>
      <input
        type="email"
        placeholder="Correo institucional"
        value={correo}
        onChange={(e) => setCorreo(e.target.value)}
      />
      <button onClick={handleLogin}>Ingresar</button>
    </div>
  );
}
