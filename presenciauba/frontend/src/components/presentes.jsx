import React, { useState, useEffect } from "react";
import axios from "axios";
import Lista from "./Lista"; 

export default function Presentes() {
  const [modo, setModo] = useState("lista");
  const [estudiantes, setEstudiantes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEstudiantes = async () => {
      try {
        const token = localStorage.getItem("token");
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

  const estudiantesFiltrados =
    modo === "presente"
      ? estudiantes.filter((e) => e.estado === "presente")
      : estudiantes;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Control de Asistencia</h2>

      <div style={{ marginBottom: "15px" }}>
        <button onClick={() => setModo("lista")}>Lista completa</button>
        <button onClick={() => setModo("presente")}>Presentes</button>
      </div>

      <Lista estudiantes={estudiantesFiltrados} /> {/* usás el componente */}
    </div>
  );
}
