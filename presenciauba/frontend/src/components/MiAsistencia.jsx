import { useEffect, useState } from "react";

function MiAsistencia() {
  const [asistencias, setAsistencias] = useState([]);
  const [porcentaje, setPorcentaje] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAsistencia = async () => {
      try {
        const token = localStorage.getItem("token");

        const response = await fetch("http://10.56.13.21:5000/mi_asistencia", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });

        if (!response.ok) {
          throw new Error("Error al obtener asistencia");
        }

        const data = await response.json();

        setAsistencias(data.asistencias);
        setPorcentaje(data.porcentaje_asistencia || 0);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAsistencia();
  }, []);

  if (loading) return <p>Cargando asistencia...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Mi Historial de Asistencia</h2>

      <h3>Porcentaje: {porcentaje}%</h3>

      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Materia</th>
            <th>Fecha</th>
            <th>Hora</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {asistencias.map((asistencia, index) => (
            <tr key={index}>
              <td>{asistencia.materia}</td>
              <td>{asistencia.fecha}</td>
              <td>{asistencia.hora}</td>
              <td
                style={{
                  color: asistencia.estado === "Presente" ? "green" : "red",
                  fontWeight: "bold"
                }}
              >
                {asistencia.estado}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default MiAsistencia;