import React, { useEffect, useState } from "react";
import {default as Slider} from '../components/Slider2/Slider';
import {default as getPrendaByTipo} from '../controllers/prendaController'
import '../views/Home.css'
export default function Home(){
    const[remeras,setRemeras] = useState([]);
    const[pantalones,setPantalones] = useState([]);

    useEffect( () => {
         getPrendaByTipo('Remera',setRemeras)
         getPrendaByTipo('Pantalon',setPantalones)
    }, []);

    return(
        <div>
            <Slider prendas={remeras} tipo='Remeras'/>
            <Slider prendas={pantalones} tipo='Pantalones'/>
        </div>
    )
}