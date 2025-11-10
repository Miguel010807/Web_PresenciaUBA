import React, { useEffect, useState } from "react";
import axios from "axios"; 

// CRÍTICO: Usamos HTTPS para el backend de Flask 
const API_BASE_URL = "https://localhost:5000"; 
// CRÍTICO: Usamos el APP_ID configurado en tu aplicación de Facebook
const APP_ID = "837039822045468"; 

// ACEPTAMOS LA FUNCIÓN DE ÉXITO DEL COMPONENTE PADRE
export default function FacebookLogin({ onLoginSuccess, sizeClass = "" }) {
  const [sdkLoaded, setSdkLoaded] = useState(false);
  const [loading, setLoading] = useState(false); 
  const [error, setError] = useState(null); 

  // ===============================================
  // 1. LÓGICA DE COMUNICACIÓN CON FLASK
  // ===============================================
  const fetchBackend = async (accessToken) => {
    setLoading(true); 
    setError(null);
    try {
      // Petición POST a la ruta HTTPS de Flask
      const response = await axios.post(`${API_BASE_URL}/auth/facebook`, {
        accessToken: accessToken,
      });

      // El backend devuelve: { message, user_id, session_token, facebook_data_debug }
      // Adaptamos la respuesta para el LoginModal
      const { session_token, facebook_data_debug } = response.data;

      //  Simulamos el rol (el backend debería manejar esto,
      // pero usamos la lógica de tu routes.py para el 'admin')
      const user_email = facebook_data_debug?.email || 'user_facebook@lumine.com';
      const role = user_email === 'admin@lumine.com' ? 'admin' : 'user';

      if (onLoginSuccess) {
        // Llama al callback del LoginModal con el objeto requerido { access_token, role }
        onLoginSuccess({ access_token: session_token, role }); 
      }
      
      console.log("Token de Flask recibido y callback ejecutado.");

    } catch (err) {
      console.error("Error al validar token de Facebook en Flask:", err.response?.data || err);
      // Muestra el mensaje de error del backend si existe
      setError(err.response?.data?.error || "Error de red o CORS al validar el token en el backend.");

    } finally {
      setLoading(false); 
    }
  };
  
  // ... (LÓGICA DEL SDK DE FACEBOOK y RENDERIZADO) ...
  // LÓGICA DE SDK DE FACEBOOK (Asegúrate de que 'checkLoginStatus' y 'login' usen 'fetchBackend')
  const checkLoginStatus = () => {
    if (!window.FB) return;
    //  QUITAR 'async' de aquí 
    window.FB.getLoginStatus(function (response) { // YA NO ES ASYNC
      if (response.status === "connected") {
        const { accessToken } = response.authResponse;
        //  Llamada a fetchBackend (que sí es async) envuelta en el callback síncrono
        fetchBackend(accessToken);
      }
    });
  };

  // Función principal de login
  const login = () => {
    if (!window.FB) {
        setError("SDK no cargado. Intente recargar.");
        return;
    }
    setLoading(true);
    setError(null);

    window.FB.login(
        // CORRECCIÓN: Quitamos 'async' para que el SDK de Facebook la acepte
        (response) => { 
            if (response.status === "connected" && response.authResponse) {
              const { accessToken } = response.authResponse;
              fetchBackend(accessToken); 
            } else {
              console.log("Usuario no conectado o permisos rechazados");
              setLoading(false);
              setError("Login cancelado o fallido.");
            }
          },
          { scope: "public_profile" } 
        );
      };

  // Cargar SDK
  useEffect(() => {
    if (window.FB) {
      setSdkLoaded(true);
      //checkLoginStatus();
      return;
    }

    window.fbAsyncInit = function () {
      window.FB.init({
        appId: APP_ID,
        cookie: true,
        xfbml: false,
        version: "v18.0",
      });
      setSdkLoaded(true);
      //checkLoginStatus();
    };

    (function (d, s, id) {
      const fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return;
      const js = d.createElement(s);
      js.id = id;
      // Nota: El SDK de Facebook debe cargarse en HTTPS
      js.src = "https://connect.facebook.net/es_LA/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    })(document, "script", "facebook-jssdk");
  }, []);

  // ===============================================
  // 3. RENDERIZADO DEL BOTÓN
  // ===============================================
  return (
    <div style={{ width: '100%', height: '100%' }}> 
      
      {/* Muestra un mensaje si el SDK no ha cargado */}
      {!sdkLoaded && <button disabled className={`btn btn-secondary ${sizeClass}`}>Cargando...</button>}

      {/* Botón de Login con Facebook */}
      {sdkLoaded && (
        <button
          onClick={login}
          disabled={loading || !sdkLoaded} 
          title="Iniciar sesión con Facebook"
          // CRÍTICO: Aplicamos la clase de tamaño (si se pasa)
          className={`btn btn-primary ${sizeClass}`} 
          style={{
            background: "#1877F2",
            borderColor: "#1877F2",
            color: "white",
            // Padding ajustado para hacerlo similar al de Google
            padding: "8px 12px", 
            borderRadius: 8,
            cursor: "pointer",
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            // Reducimos la fuente para compactar
            fontSize: '14px', 
            fontWeight: '600',
            opacity: loading ? 0.7 : 1,
          }}
        >
          {/* ... (El contenido interno del botón) ... */}
           {loading ? (
             <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true" style={{marginRight: '8px'}}></span>
          ) : (
             <i className="bi bi-facebook" style={{marginRight: '8px', fontSize: '18px'}}></i> 
          )}
          Iniciar sesión con Facebook
        </button>
      )}
      
      {/* Muestra errores debajo del botón */}
      {error && <div className="text-danger small mt-1 text-center">{error}</div>}
    </div>
  );
}