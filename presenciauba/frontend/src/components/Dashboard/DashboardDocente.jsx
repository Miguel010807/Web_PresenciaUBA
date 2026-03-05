import React, { useState } from "react";
import { Home, QrCode, Clock, LogOut } from "lucide-react"; // <- librería de íconos
import "./DashboardDocente.css";
import CambiarContraseña from "../CambiarContraseña";
import CambiarNumero from "../CambiarNumero";

function DashboardDocente({ usuario, onLogout }) {
  const [formData, setFormData] = useState({
    numero_aula: "",
    curso: "A",
    materia: "",
    fecha: "",
  });

  const [qrImage, setQrImage] = useState(null);
  const [mensaje, setMensaje] = useState("");
  const [activeSection, setActiveSection] = useState("home");

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
      const token = localStorage.getItem("token");

  const res = await fetch("http://10.56.13.31:5000/generar_qr", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify(formData),
});

      const data = await res.json();

      if (res.ok) {
        setQrImage(`data:image/png;base64,${data.qr}`);
        setMensaje("QR generado con éxito.");
      } else {
        setMensaje("Error al generar el QR.");
      }
    } catch (error) {
      console.error(error);
      setMensaje("No se pudo conectar con el servidor.");
    }
  };

  return (
    <div className="dashboard-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2 className="sidebar-title">Docente</h2>
        <ul className="sidebar-menu">
          <li
            className={activeSection === "home" ? "active" : ""}
            onClick={() => setActiveSection("home")}
          >
            <Home size={20} />
            <span>Inicio</span>
          </li>
          <li
            className={activeSection === "qr" ? "active" : ""}
            onClick={() => setActiveSection("qr")}
          >
            <QrCode size={20} />
            <span>Generar QR</span>
          </li>
          <li
            className={activeSection === "historial" ? "active" : ""}
            onClick={() => setActiveSection("historial")}
          >
            <Clock size={20} />
            <span>Historial</span>
          </li>
          <li
            className={activeSection === "config" ? "active" : ""}
            onClick={() => setActiveSection("config")}
          >
            <span>Configuración</span>
          </li>
          <li onClick={onLogout}>
            <LogOut size={20} />
            <span>Salir</span>
          </li>
        </ul>
      </aside>

      {/* Contenido principal */}
      <main className="main-content">
        {activeSection === "home" && (
          <div>
            <h1>Bienvenido Docente {usuario.nombre}</h1>
            <p>Rol: {usuario.rol}</p>
          </div>
        )}

        {activeSection === "qr" && (
          <div>
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
              <select
                name="curso"
                value={formData.curso}
                onChange={handleChange}
              >
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
        )}

        {activeSection === "historial" && (
          <div>
            <h2>Historial de QRs generados</h2>
            <p>
              📜 Aquí podrías listar los QR guardados desde la base de datos.
            </p>
          </div>
        )}
        {activeSection === "config" && (
          <div>
            <h2>⚙️ Configuración</h2>
            <CambiarContraseña usuario={usuario} />
            <CambiarNumero usuario={usuario} />
          </div>
        )}
      </main>
    </div>
  );
}

export default DashboardDocente;
