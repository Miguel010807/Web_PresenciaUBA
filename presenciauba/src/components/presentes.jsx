import React, { useState, useEffect } from "react";
import axios from "axios";

export default function Presentes() {
  // Estado para saber si mostramos la lista completa o solo los presentes
  const [modo, setModo] = useState("lista"); // "lista" o "presente"

  // Estado donde guardamos los estudiantes traídos desde el backend
  const [estudiantes, setEstudiantes] = useState([]);

  // Estado de carga (para mostrar "Cargando..." mientras esperamos la API)
  const [loading, setLoading] = useState(true);

  // Se ejecuta al cargar el componente (similar a componentDidMount en clases)
  useEffect(() => {
    const fetchEstudiantes = async () => {
      try {
        // Recuperamos el token guardado en el login
        const token = localStorage.getItem("token");

        // Llamamos al backend para traer la lista de asistencias
        const res = await axios.get("http://localhost:5000/api/asistencias", {
          headers: { Authorization: `Bearer ${token}` }, // protegemos con JWT
        });

        // Guardamos los estudiantes en el estado
        setEstudiantes(res.data);
      } catch (error) {
        console.error("Error cargando estudiantes", error);
      } finally {
        // Dejamos de mostrar el "Cargando..."
        setLoading(false);
      }
    };

    fetchEstudiantes(); // ejecutamos la función al iniciar
  }, []);

  // Mientras la API está cargando mostramos un texto
  if (loading) return <p>Cargando...</p>;

  // Filtramos según el modo elegido:
  // - Si el modo es "presente", dejamos solo los que tienen estado === "presente"
  // - Si es "lista", mostramos todos
  const estudiantesFiltrados =
    modo === "presente"
      ? estudiantes.filter((e) => e.estado === "presente")
      : estudiantes;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Control de Asistencia</h2>

      {/* Botones para alternar entre modos */}
      <div style={{ marginBottom: "15px" }}>
        {/* Cambia el estado "modo" a "lista" */}
        <button onClick={() => setModo("lista")}>Lista completa</button>

        {/* Cambia el estado "modo" a "presente" */}
        <button onClick={() => setModo("presente")}>Presentes</button>
      </div>

      {/* Mostramos los estudiantes en una tabla */}
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {/* Recorremos los estudiantes filtrados */}
          {estudiantesFiltrados.map((est) => (
            <tr key={est.id_usuario}>
              <td>{est.nombre}</td>
              <td>{est.apellido}</td>
              <td
                style={{
                  // Verde si está presente, rojo si está ausente
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
