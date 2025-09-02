import React, { useState } from "react";
import Login from "./components/Login";
import QRScanner from "./components/QRScanner";
import StatusCard from "./components/StatusCard";

export default function App() {
  const [usuario, setUsuario] = useState(null);

  return (
    <div className="app">
      {!usuario ? (
        <Login setUsuario={setUsuario} />
      ) : (
        <>
          <StatusCard usuario={usuario} />
          <QRScanner usuario={usuario} />
        </>
      )}
    </div>
  );
}
