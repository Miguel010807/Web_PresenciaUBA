import { useEffect, useState } from "react";
import "./App.css";
import { Operator } from "./components/operator";


function App() {
 const [count, setCount] = useState(0);


 useEffect(() => {
   //useEffect ejecuta el codigo una vez si no hay nada en los
   //corchetes, y si hay variables(dependencias)
   //se va a ejecutar tanto como actualice
 }, []);


 return (
   <>
     <Operator />
   </>
 );
}


export default App;