import React from "react";
import { registrarAsistenciaGeneral } from "../api";

export default function StatusCard({ usuario }) {
  const handleGeneral = async () => {
    await registrarAsistenciaGeneral(usuario.id);
    alert("Presencia general registrada");
  };

  return (
    <div>
      <h2>Bienvenido, {usuario.nombre}</h2>
      <button onClick={handleGeneral}>Registrar entrada</button>
    </div>
  );
}
