import React, { useEffect, useState } from "react";
import { default as Slider } from "../components/Slider2/Slider";
import {getPrendaByTipo,getPrendaByTipoAndGenero} from "../controllers/prendaController";
import "../views/Home.css";
import ResponsiveAppBar from "../components/AppBar";
import { Container } from "@mui/system";

export default function Home() {
  const [remeras, setRemeras] = useState([]);
  const [pantalones, setPantalones] = useState([]);
  const [calzados, setCalzado] = useState([]);
  const genero = localStorage.getItem("genero")
  
  useEffect(() => {
    getPrendaByTipo("Remera", setRemeras , genero);
    getPrendaByTipo("Pantalon", setPantalones, genero);
    getPrendaByTipo("Calzados", setCalzado , genero);
  }, []);

  return (
    <div className="app-container">
      <ResponsiveAppBar />
      <div>
        <Container maxWidth="xl">
          <div>
            <Slider prendas={remeras} tipo="Remeras" />
            <Slider prendas={pantalones} tipo="Pantalones" />
            <Slider prendas={calzados} tipo="Calzados" />
          </div>
        </Container>
      </div>
    </div>
  );
}
