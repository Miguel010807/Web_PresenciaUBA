import { useState } from "react"; // Hook de React para manejar estados locales
import api from "../api"; // Importa el archivo de configuración de Axios (para hablar con el backend)

// Componente de Login.
function Login({ onLogin }) {
  // Estados para manejar los inputs y errores
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // Función que se ejecuta al enviar el formulario
  const handleSubmit = async (e) => {
    e.preventDefault(); // evita que la página se recargue

    try {
      // Se hace una petición POST al backend con correo y password
      const res = await api.post("/login", { correo, password });

      // Si la respuesta es correcta, guardamos el token en localStorage
      localStorage.setItem("token", res.data.token);

      // Llamamos a la función pasada por props para avisar que el login fue exitoso
      onLogin(res.data.usuario);
    } catch (err) {
      // Si algo falla, mostramos un mensaje de error
      setError("Credenciales inválidas o no conectado al WiFi institucional.");
    }
  };

  return (
    <div className="login-container">
      <h2>Presencia UBA</h2>
      <form onSubmit={handleSubmit}>
        {/* Input del correo institucional */}
        <input
          type="email"
          placeholder="Correo institucional"
          value={correo}
          onChange={(e) => setCorreo(e.target.value)} // Actualiza estado cuando el usuario escribe
          required
        />

        {/* Input de la contraseña */}
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)} // Actualiza estado cuando el usuario escribe
          required
        />

        {/* Botón de login */}
        <button type="submit">Iniciar sesión</button>

        {/* Si hay un error, lo mostramos debajo del formulario */}
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}

export default Login; // Exportamos el componente para usarlo en App.jsx
