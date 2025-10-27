import React, { useState } from "react";
import "./DashboardDocente.css";

function DashboardDocente({ usuario, onLogout }) {
  const [formData, setFormData] = useState({
    numero_aula: "",
    curso: "A",
    materia: "",
    fecha: "",
  });

  const [qrImage, setQrImage] = useState(null);
  const [mensaje, setMensaje] = useState("");

  // Maneja los cambios en los inputs
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Envía los datos al backend y genera el QR
  const generarQR = async () => {
    if (!formData.numero_aula || !formData.materia || !formData.fecha) {
      setMensaje("Por favor, complete todos los campos.");
      return;
    }

    try {
      const res = await fetch("http://10.56.2.53:5000/generar_qr", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (res.ok) {
        setQrImage(`data:image/png;base64,${data.qr_image}`);
        setMensaje("QR generado con exito.");
      } else {
        setMensaje("Error al generar el QR.");
      }
    } catch (error) {
      console.error(error);
      setMensaje("No se pudo conectar con el servidor.");
    }
  };

  return (
    <div className="dashboard-container">
      <h1>Bienvenido Docente {usuario.nombre}</h1>
      <p>Rol: {usuario.rol}</p>

      <button onClick={onLogout}>Cerrar sesión</button>

      <hr />

      <h2>Generar QR de Clase</h2>

      <div className="form-container">
        <label>Número de Aula:</label>
        <input
          type="text"
          name="numero_aula"
          value={formData.numero_aula}
          onChange={handleChange}
          placeholder="Ej: 203"
        />

        <label>Curso:</label>
        <select name="curso" value={formData.curso} onChange={handleChange}>
          <option value="A">5-A</option>
          <option value="B">5-B</option>
          <option value="C">5-C</option>
          <option value="D">5-D</option>
        </select>

        <label>Materia:</label>
        <input
          type="text"
          name="materia"
          value={formData.materia}
          onChange={handleChange}
          placeholder="Ej: Matemática"
        />

        <label>Fecha:</label>
        <input
          type="date"
          name="fecha"
          value={formData.fecha}
          onChange={handleChange}
        />

        <button onClick={generarQR}>Generar QR</button>

        {mensaje && <p>{mensaje}</p>}
      </div>

      {qrImage && (
        <div className="qr-section">
          <h3>QR Generado:</h3>
          <img
            src={qrImage}
            alt="QR generado"
            style={{ width: "200px", marginTop: "10px" }}
          />
        </div>
      )}
    </div>
  );
}

export default DashboardDocente;