import React, { useState, useEffect } from "react";
import axios from "axios";

export default function Presentes() {
  const [modo, setModo] = useState("lista"); // "lista" o "presente"
  const [estudiantes, setEstudiantes] = useState([]);
  const [loading, setLoading] = useState(true);

  // Simulación: al entrar al componente se consulta la API
  useEffect(() => {
    const fetchEstudiantes = async () => {
      try {
        const token = localStorage.getItem("token"); // token del login
        const res = await axios.get("http://localhost:5000/api/asistencias", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setEstudiantes(res.data);
      } catch (error) {
        console.error("Error cargando estudiantes", error);
      } finally {
        setLoading(false);
      }
    };

    fetchEstudiantes();
  }, []);

  if (loading) return <p>Cargando...</p>;

  // Filtrar según el modo
  const estudiantesFiltrados =
    modo === "presente"
      ? estudiantes.filter((e) => e.estado === "presente")
      : estudiantes;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Control de Asistencia</h2>

      {/* Botones para cambiar modo */}
      <div style={{ marginBottom: "15px" }}>
        <button onClick={() => setModo("lista")}>Lista completa</button>
        <button onClick={() => setModo("presente")}>Solo presentes</button>
      </div>

      {/* Tabla de estudiantes */}
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {estudiantesFiltrados.map((est) => (
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
    </div>
  );
}
