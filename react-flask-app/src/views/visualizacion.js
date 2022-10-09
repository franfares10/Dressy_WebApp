import React,{useState} from "react";
import { useLocation } from 'react-router-dom'
import{Routes,Route,Link, Router,BrowserRouter} from 'react-router-dom'
import stopThreads from "../controllers/concurrencyController";
import './visualizacion.css'


export default function Visualizacion (){
    const location = useLocation()
    let procesar = location.state[1]
    let prenda = location.state[0]
    //Uso la descripcion como ID unico.
    console.log("La prenda que eligió el user: "+JSON.stringify(location.state[0]))  
    console.log(procesar)

return(
    <div className="container-prediction-image">
        <img src={'/video_feed?prenda='+prenda.descripcion+'&tipo='+prenda.tipo+'&marca='+prenda.marca.nombre+'&procesar='+procesar}/>
        <Link to={'/'}>
        <button onClick={() =>{
        procesar = 0
        stopThreads(prenda,0)
        }}>Volver</button>
        </Link>
    </div>
    
)
}