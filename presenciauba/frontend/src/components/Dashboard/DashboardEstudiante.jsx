import React, { useState, useRef, useEffect } from "react";
import QrScanner from "qr-scanner";
import {
  FaHome,
  FaHistory,
  FaQrcode,
  FaCog,
  FaSignOutAlt,
} from "react-icons/fa";
import "./DashboardEstudiante.css";
import CambiarContraseña from "../CambiarContraseña";

function DashboardEstudiante({ usuario, onLogout }) {
  const [escaneando, setEscaneando] = useState(false);
  const [mensaje, setMensaje] = useState("");
  const [vista, setVista] = useState("home");
  const videoRef = useRef(null);
  const scannerRef = useRef(null);

  useEffect(() => {
    if (escaneando && videoRef.current) {
      const scanner = new QrScanner(
        videoRef.current,
        async (result) => {
          if (result?.data) {
            try {
              const dataQR = JSON.parse(result.data);

              const res = await fetch(
                "http://10.56.2.56:5000/registrar_asistencia",
                {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                    id_usuario: usuario.id,
                    id_materia: dataQR.id_materia,
                    dispositivo: "web",
                  }),
                }
              );

              const data = await res.json();
              setMensaje(data.message);
            } catch (error) {
              console.error(error);
              setMensaje("⚠️ Error al registrar asistencia o leer el QR.");
            } finally {
              setEscaneando(false);
              scanner.stop();
            }
          }
        },
        { returnDetailedScanResult: true }
      );

      scanner.start();
      scannerRef.current = scanner;

      return () => {
        scanner.stop();
      };
    }
  }, [escaneando]);

  return (
    <div className="dashboard-layout">
      {/* --- Barra lateral --- */}
      <aside className="sidebar">
        <h2 className="sidebar-title">Estudiante</h2>
        <ul className="sidebar-menu">
          <li
            className={vista === "home" ? "active" : ""}
            onClick={() => setVista("home")}
          >
            <FaHome size={18} />
            <span>Inicio</span>
          </li>
          <li
            className={vista === "historial" ? "active" : ""}
            onClick={() => setVista("historial")}
          >
            <FaHistory size={18} />
            <span>Historial</span>
          </li>
          <li
            className={vista === "escanear" ? "active" : ""}
            onClick={() => setVista("escanear")}
          >
            <FaQrcode size={18} />
            <span>Escanear QR</span>
          </li>
          <li
            className={vista === "config" ? "active" : ""}
            onClick={() => setVista("config")}
          >
            <FaCog size={18} />
            <span>Configuración</span>
          </li>
          <li onClick={onLogout}>
            <FaSignOutAlt size={18} />
            <span>Salir</span>
          </li>
        </ul>
      </aside>

      {/* --- Contenido principal --- */}
      <main className="main-content">
        <h1>Bienvenido, {usuario.nombre}</h1>

        {vista === "home" && (
          <p>Seleccioná una opción del menú para comenzar.</p>
        )}

        {vista === "escanear" && (
          <div className="qr-section">
            {!escaneando ? (
              <button className="btn" onClick={() => setEscaneando(true)}>
                📷 Iniciar escaneo
              </button>
            ) : (
              <div>
                <video
                  ref={videoRef}
                  style={{ width: "100%", borderRadius: "8px" }}
                />
                <button
                  className="btn cancel"
                  onClick={() => setEscaneando(false)}
                >
                  Cancelar
                </button>
              </div>
            )}
            {mensaje && <p className="mensaje">{mensaje}</p>}
          </div>
        )}

        {vista === "historial" && (
          <div>
            <h2>📜 Historial de asistencias</h2>
            <p>
              (Acá se mostrarán las asistencias registradas desde la base de
              datos.)
            </p>
          </div>
        )}

        {vista === "config" && (
          <div>
            <h2>⚙️ Configuración</h2>
            <CambiarContraseña usuario={usuario} />
          </div>
        )}
      </main>
    </div>
  );
}

export default DashboardEstudiante;
