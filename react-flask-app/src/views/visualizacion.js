import { Button, CircularProgress, Grid, Item } from "@mui/material";
import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import { Routes, Route, Link, Router, BrowserRouter } from "react-router-dom";
import LoadingCard from "../components/LoadingCard";
import stopThreads from "../controllers/concurrencyController";
import ejemplo from "../assets/Pagina4.png";
import ejemplo2 from "../assets/Pagina5.png";
import ResponsiveAppBar from "../components/AppBar";
import "./visualizacion.css";
import { height, width } from "@mui/system";
/* ESTA VA PRIMERO<img
          src={"/unity_image"}
          width={640}
          height={480}
          id="Unity"
          style={{ visibility: "visible" }}
        />
        
         <img
        src={
          "/video_feed?prenda=" +
          prenda._id +
          "&tipo=" +
          prenda.tipo +
          "&marca=" +
          prenda.marca.nombre +
          "&procesar=" +
          procesar
        }
        id="imagenUser"
        style={{ visibility: "visible" }}
      />
        */

const checkTime = (setCanShow) => {
  try {
    let imagen = document.querySelector("#imagenUser");
    let result = imagen.complete;
    if (result === false) {
      //No cargo la imagen todavía, lo dejo como esta.
    } else {
      setCanShow(true);
    }
  } catch (e) {
    console.log(e);
  }
};

const turnOnFacialRecognition = (showFacial, setShowFacial) => {
  let width = window.screen.width;
  let height = window.screen.height * 0.78;

  if (!showFacial) {
    console.log("Oculta unity y muestra AI");
    document.querySelector("#imagenUser").style.visibility = "visible";
    document.querySelector("#imagenUser").style.height = height.toString()+'px';
    document.querySelector("#imagenUser").style.width = width.toString()+'px';
    document.querySelector("#Unity").style.visibility = "hidden";
    document.querySelector("#Unity").style.height = "0px";
    document.querySelector("#Unity").style.width = "0px";
    setShowFacial(true);
  } else {
    console.log("Oculta AI y muestra Unity");
    document.querySelector("#imagenUser").style.visibility = "hidden";
    document.querySelector("#imagenUser").style.height = "0px";
    document.querySelector("#imagenUser").style.width = "0px";
    document.querySelector("#Unity").style.visibility = "visible";
    document.querySelector("#Unity").style.height = height.toString()+'px';
    document.querySelector("#Unity").style.width = width.toString()+'px';
    setShowFacial(false);
  }
};
export default function Visualizacion() {
  const location = useLocation();
  const [canShow, setCanShow] = useState(false);
  const [showFacial, setShowFacial] = useState(false);

  const handleOnOpen = () => {
    console.log("Arranca por aca titanbnn");
    setCanShow(true);
  };
  let width = window.screen.width;
  let height = window.screen.height * 0.78;
  let procesar = location.state[1];
  let prenda = location.state[0];
  setInterval(function () {
    checkTime(setCanShow);
    //Borrar si no funca
  }, 1000);
  return (
    <div className="container-prediction-image">
      <ResponsiveAppBar />
      {!canShow ? (
        <LoadingCard />
      ) : (
        //aca va la primera
        <img
          className="img-realidad-aumentada"
          id="Unity"
          src={"/unity_image"}
          style={{ visibility: "visible", height: height, width: width }}
        />
      )}

      <img
        className="img-inteligencia-artificial"
        src={
          "/video_feed?prenda=" +
          prenda._id +
          "&tipo=" +
          prenda.tipo +
          "&marca=" +
          prenda.marca.nombre +
          "&procesar=" +
          procesar
        }
        id="imagenUser"
        style={{ visibility: "hidden", height: "0px", width: "0px" }}
      />
      <div className="buttons-container">
        <Button
          variant="contained"
          onClick={(e) => {
            e.preventDefault();
            turnOnFacialRecognition(showFacial, setShowFacial);
          }}
          style={{ display: "block", marginBottom: "5%" }}
        >
          {!showFacial ? ("Mostrar reconocimiento facial") : ("Ocultar reconocimiento facial")}
        </Button>

        <Button
          variant="contained"
          color="error"
          onClick={() => {
            procesar = 0;
            stopThreads(prenda, 0);
            window.history.go("-1");
          }}
          style={{ display: "block", marginBottom: "2%", float: "right" }}
        >
          Volver
        </Button>
      </div>
    </div>
  );
}
