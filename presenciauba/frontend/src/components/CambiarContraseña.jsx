import { useState } from "react";

function CambiarContraseña({ usuario }) {
  const [actual, setActual] = useState("");
  const [nueva, setNueva] = useState("");
  const [mensaje, setMensaje] = useState("");

  const handleCambiar = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("token");

      const res = await fetch("http://10.56.2.58:5000/cambiar_contrasena", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // el token que esta aca es como un pasaporte, si no te genera el token no podes pasar al dashboard
        },
        body: JSON.stringify({
          id_usuario: usuario.id_usuario ,
          actual: actual,
          nueva: nueva,
        }),
      });

      const data = await res.json();
      setMensaje(data.message || "Contraseña actualizada correctamente.");
    } catch (error) {
      console.error(error);
      setMensaje("Error al cambiar la contraseña.");
    }
  };

  return (
    <div className="cambiar-container">
      <h3>Cambiar contraseña</h3>
      <form onSubmit={handleCambiar} className="cambiar-form">
        <label>Contraseña actual:</label>
        <input
          type="password"
          value={actual}
          onChange={(e) => setActual(e.target.value)}
          required
        />

        <label>Nueva contraseña:</label>
        <input
          type="password"
          value={nueva}
          onChange={(e) => setNueva(e.target.value)}
          required
        />

        <button type="submit">Guardar</button>
      </form>

      {mensaje && <p className="mensaje">{mensaje}</p>}
    </div>
  );
}

export default CambiarContraseña;
