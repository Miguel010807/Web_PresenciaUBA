import { useState } from "react";

function CambiarNumero() {
  const [numeroActual, setNumeroActual] = useState("");
  const [numeroNuevo, setNumeroNuevo] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMensaje("");
    setError("");

    try {
      const token = localStorage.getItem("token");

      const response = await fetch("http://10.56.13.21:5000/cambiar_numero", {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          numero_actual: numeroActual,
          numero_nuevo: numeroNuevo
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Error al actualizar número");
      }

      setMensaje("Número actualizado correctamente ✅");
      setNumeroActual("");
      setNumeroNuevo("");

    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ marginTop: "40px" }}>
      <h3>Cambiar número</h3>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Número actual:</label>
          <input
            type="text"
            value={numeroActual}
            onChange={(e) => setNumeroActual(e.target.value)}
            required
          />
        </div>

        <div style={{ marginTop: "10px" }}>
          <label>Nuevo número:</label>
          <input
            type="text"
            value={numeroNuevo}
            onChange={(e) => setNumeroNuevo(e.target.value)}
            required
          />
        </div>

        <button
          type="submit"
          style={{
            marginTop: "15px",
            padding: "8px 15px",
            backgroundColor: "#0d3b66",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer"
          }}
        >
          Guardar
        </button>
      </form>

      {mensaje && <p style={{ color: "green" }}>{mensaje}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default CambiarNumero;