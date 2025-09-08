import axios from "axios";

const API = "http://127.0.0.1:5000";

export const login = async (correo) => {
  const res = await axios.post(`${API}/login`, { correo });
  return res.data;
};

export const registrarAsistenciaGeneral = async (usuario_id) => {
  const res = await axios.post(`${API}/asistencia/general`, { usuario_id });
  return res.data;
};

export const registrarAsistenciaMateria = async (usuario_id, materia_id) => {
  const res = await axios.post(`${API}/asistencia/materia`, {
    usuario_id,
    materia_id,
  });
  return res.data;
};
