import { Button, CircularProgress } from "@mui/material";
import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import { Routes, Route, Link, Router, BrowserRouter } from "react-router-dom";
import LoadingCard from "../components/LoadingCard";
import stopThreads from "../controllers/concurrencyController";
import "./visualizacion.css";

export default function Visualizacion() {
  const location = useLocation();
  const [canShow, setCanShow] = useState(false);
  const [showFacial, setShowFacial] = useState(false);

  const handleOnOpen = () => {
    console.log("Arranca por aca titanbnn");
    setCanShow(true);
  };

  let procesar = location.state[1];
  let prenda = location.state[0];

  return (
    <div className="container-prediction-image">
      {
        //Preguntarle al fares si sabe como borrar el numero que retorna este setInterval. Es tipo un id que retorna siempre.
        //Preguntar lo del index a fran.

        setInterval(function () {
          checkTime(setCanShow);
          //Borrar si no funca
        }, 1000)
      }
      {!canShow ? (
        <LoadingCard />
      ) : (
        <img
          src={"/unity_image"}
          width={640}
          height={480}
          id="Unity"
          style={{ visibility: "visible" }}
        />
      )}

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

      <Button
      variant="outlined"
        onClick={() => {
          procesar = 0;
          stopThreads(prenda, 0);
          window.history.go("-1");
        }}
      >
        Volver
      </Button>

      <Button
        variant="contained"
        onClick={(e) => {
          e.preventDefault();
          turnOnFacialRecognition(showFacial, setShowFacial);
        }}
      >
        Ver reconocimiento facial
      </Button>
    </div>
  );
}

const checkTime = (setCanShow) => {
  try {
    let imagen = document.querySelector("#imagenUser");
    let result = imagen.complete;
    if (result === false) {
      //No cargo la imagen todavía, lo dejo como esta.
    } else {
      console.log("Paso por aca");
      setCanShow(true);
    }
  } catch (e) {
    console.log(e);
  }
};

const turnOnFacialRecognition = (showFacial, setShowFacial) => {
  console.log("Entro");
  if (!showFacial) {
    console.log("NO ENTRO ACA");
    document.querySelector("#imagenUser").style.visibility = "visible";
    document.querySelector("#Unity").style.visibility = "hidden";
    setShowFacial(true);
  } else {
    console.log("No entro aca");
    document.querySelector("#imagenUser").style.visibility = "hidden";
    document.querySelector("#Unity").style.visibility = "visible";
    setShowFacial(false);
  }
};
