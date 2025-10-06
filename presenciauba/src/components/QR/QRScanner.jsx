import { useState } from "react";
import { QrReader } from "react-qr-reader";
import api from "../../api";

function QRScanner() {
  const [resultado, setResultado] = useState("");

  const handleScan = async (data) => {
    if (data) {
      try {
        const token = localStorage.getItem("token");
        const res = await api.post(
          "/asistencia/materia",
          { qr_code: data },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setResultado("Asistencia registrada: " + res.data.materia);
      } catch (err) {
        setResultado("Error al registrar asistencia");
      }
    }
  };

  return (
    <div className="qrscanner-container">
      <h3>Escanear código QR del aula</h3>
      <QrReader
        onResult={(result, error) => {
          if (!!result) {
            handleScan(result?.text);
          }
        }}
        style={{ width: "100%" }}
      />
      <p>{resultado}</p>
    </div>
  );
}

export default QRScanner;
