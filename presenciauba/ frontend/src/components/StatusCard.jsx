function StatusCard({ usuario, conectado }) {
  return (
    <div className="status-card">
      <h4>Estado de sesión</h4>
      {usuario ? (
        <p>
          {usuario.nombre} {usuario.apellido} ({usuario.rol})
        </p>
      ) : (
        <p>No autenticado</p>
      )}
      <p>{conectado ? "Conectado a WiFi UBA" : "No conectado"}</p>
    </div>
  );
}

export default StatusCard;
