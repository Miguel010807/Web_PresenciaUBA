import Login from "./components/Login";

function MyButton() {
  return <button>Soy un botón</button>;
}

export default function MyApp() {
  return (
    <div>
      <h1>Bienvenido a mi aplicación</h1>
      <MyButton />
      <Login />
    </div>
  );
}
