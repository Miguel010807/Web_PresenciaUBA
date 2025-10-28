import React, { useEffect, useRef, useState } from "react";
import QrScanner from "qr-scanner";

function EscanearQR({ usuario }) {
  const videoRef = useRef(null);
  const [resultado, setResultado] = useState("");
  const [scanner, setScanner] = useState(null);

  useEffect(() => {
    if (videoRef.current) {
      const qrScanner = new QrScanner(
        videoRef.current,
        (result) => {
          setResultado(result.data);
          qrScanner.stop();
          registrarAsistencia(result.data);
        },
        { highlightScanRegion: true }
      );
      qrScanner.start();
      setScanner(qrScanner);
    }

    return () => {
      if (scanner) scanner.stop();
    };
  }, []);

  const registrarAsistencia = async (qrData) => {
    try {
      const response = await fetch("http://10.56.2.48:5000/registrar_asistencia", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id_usuario: usuario.id_usuario,
          qr_data: qrData,
        }),
      });

      const data = await response.json();
      alert(data.message || "Asistencia registrada correctamente");
    } catch (error) {
      console.error("Error al registrar asistencia:", error);
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h2>Escanear QR</h2>
      <video
        ref={videoRef}
        style={{ width: "100%", maxWidth: "400px", borderRadius: "10px" }}
      ></video>
      {resultado && <p>QR Detectado: {resultado}</p>}
    </div>
  );
}

export default EscanearQR;