import React, { useEffect, useRef, useState } from "react";
import QrScanner from "qr-scanner";

function EscanearQR() {
  const videoRef = useRef(null);
  const scannerRef = useRef(null);
  const [resultado, setResultado] = useState("");
  const [mensaje, setMensaje] = useState("");

  useEffect(() => {
    if (!videoRef.current) return;

    const qrScanner = new QrScanner(
      videoRef.current,
      async (result) => {
        const qrUrl = result.data; // 👉 URL completa del QR
        setResultado(qrUrl);
        qrScanner.stop();

        await registrar_asistencia(qrUrl);
      },
      { highlightScanRegion: true }
    );

    qrScanner.start();
    scannerRef.current = qrScanner;

    return () => {
      qrScanner.stop();
    };
  }, []);

  const registrar_asistencia = async (qrUrl) => {
    try {
      const token = localStorage.getItem("token");

      if (!token) {
        setMensaje("No estás autenticado");
        return;
      }

      const response = await fetch(qrUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (!response.ok) {
        setMensaje(data.error || "Error al registrar asistencia");
        return;
      }

      setMensaje(data.message || "Asistencia registrada correctamente");
    } catch (error) {
      console.error("Error al registrar asistencia:", error);
      setMensaje("Error de conexión con el servidor");
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h2>Escanear QR</h2>

      <video
        ref={videoRef}
        style={{
          width: "100%",
          maxWidth: "400px",
          borderRadius: "10px",
          border: "2px solid #ccc"
        }}
      />

      {resultado && (
        <p style={{ marginTop: "10px", fontSize: "12px" }}>
          QR detectado
        </p>
      )}

      {mensaje && (
        <p style={{ marginTop: "15px", fontWeight: "bold" }}>
          {mensaje}
        </p>
      )}
    </div>
  );
}

export default EscanearQR;