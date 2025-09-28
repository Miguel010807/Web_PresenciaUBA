import React from "react";

export default function Lista({ estudiantes }) {
  return (
    <table border="1" cellPadding="10">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Apellido</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        {estudiantes.map((est) => (
          <tr key={est.id_usuario}>
            <td>{est.nombre}</td>
            <td>{est.apellido}</td>
            <td
              style={{
                color: est.estado === "presente" ? "green" : "red",
                fontWeight: "bold",
              }}
            >
              {est.estado}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
