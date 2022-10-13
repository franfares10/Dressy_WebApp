import React,{useState} from "react";
import { useLocation } from 'react-router-dom'
import{Routes,Route,Link, Router,BrowserRouter} from 'react-router-dom'
import stopThreads from "../controllers/concurrencyController";
import './UnityRenderer.css'


export default function Visualizacion (){
    const location = useLocation()

return(
    <div className="container-prediction-image">
        <img src={'/unity_image'}/>
        
        
        <Link to={'/'}>
        <button onClick={() =>{
            stopThreads("prenda",0)
        }}>Volver</button>
        </Link>
    </div>
    
)
}