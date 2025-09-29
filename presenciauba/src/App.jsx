import { useState } from "react";
import Login from "./components/Login/Login";

function App() {
  const [usuario, setUsuario] = useState(null);

  const handleLogin = (user) => {
    console.log("Usuario logueado:", user);
    setUsuario(user);
  };

  return (
    <div>
      {!usuario ? (
        <Login onLogin={handleLogin} /> //<--- si no hay usuario te muestra esto
      ) : (
        <div>
          <h1>Bienvenido {usuario.nombre}</h1>
          <button
            onClick={() => {
              localStorage.removeItem("token"); //<-- si hay usuario te muestra esto
              localStorage.removeItem("usuario");
              setUsuario(null);
            }}
          >
            Cerrar sesión
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
