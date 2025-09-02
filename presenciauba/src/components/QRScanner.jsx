import React, { useState } from "react";
import { registrarAsistenciaMateria } from "../api";

function QRScanner({ user, setStatus }) {
  const [qrCode, setQrCode] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!qrCode) return;

    try {
      // Llamamos al backend para registrar la asistencia en la materia
      const data = await registrarAsistenciaMateria(user.id_usuario, qrCode);
      setStatus({
        materia: data.materia || qrCode,
        fecha: data.fecha || new Date().toLocaleDateString(),
        hora: data.hora || new Date().toLocaleTimeString(),
      });
      setQrCode("");
    } catch (err) {
      alert("Error al registrar la asistencia");
    }
  };

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h2>Escanear QR del aula</h2>
      <input
        type="text"
        placeholder="Ingrese código QR"
        value={qrCode}
        onChange={(e) => setQrCode(e.target.value)}
        required
      />
      <button type="submit">Registrar Asistencia</button>
    </form>
  );
}

export default QRScanner;
