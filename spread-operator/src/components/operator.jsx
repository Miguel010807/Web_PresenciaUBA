import { useState } from "react";

export function Operator() {
  const [nums, setNums] = useState([1, 2, 3, 4, 5]);
  const [persona, setPersona] = useState({
    name: "Federico",
    alumno: "Thiago",
  });
  const [productos, setProductos] = useState([
    {
      nombre: "Camiseta",
      precio: 20,
    },

    { nombre: "Pantalon", precio: 30 },
  ]);

  //arrow function
  const addNums = () => {
    const ultimo = nums[nums.length - 1]; //<---- Este const me dice el ultimo numero del Array
    setNums([...nums, ultimo + 1]);
  };
  // no use "setNums ([...nums.length + 1]);" porque en el caso que sean numeros mas grandes
  // no iva afuncionar, osea si, pero no
  // por que la el "nums.length" te dice la cantidad de elementos adentros
  // del Array, y no el valor de los elementos

  const updateName = () => {
    setPersona({ ...persona, name: "Miguel", edad: 80 });
    console.log(persona);
  };

  const updateDescuentoCorrecto = () => {
    const newArr = productos.map((item) => ({
      ...item,
      descuento: true,
    }));
    console.log(newArr);
    setProductos(newArr);
  };

  /*
  
  const updateDescuento = () => {
    const newArr = productos.map((item) => {
      setProductos([{ ...item, descuento: true }]);
    });
    console.log(newArr);
  };
  
  */

  return (
    <>
      {nums.map((num, index) => (
        <p key={index}>{num}</p>
      ))}
      <h3>Spread Operator</h3>
      <button onClick={addNums}>agregar numeros</button>
      <button onClick={updateName}>modificar persona</button>
      <button onClick={updateDescuentoCorrecto}> ponerDescuento </button>
    </>
  );
}
