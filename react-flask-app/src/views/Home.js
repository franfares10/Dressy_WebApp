import React, { useEffect, useState } from "react";
import { default as Slider } from "../components/Slider2/Slider";
import { default as getPrendaByTipo } from "../controllers/prendaController";
import "../views/Home.css";
import ResponsiveAppBar from "../components/AppBar";
import { Container } from "@mui/system";

export default function Home() {
  const [remeras, setRemeras] = useState([]);
  const [pantalones, setPantalones] = useState([]);
  const [calzados, setCalzado] = useState([]);

  useEffect(() => {
    getPrendaByTipo("Remera", setRemeras);
    getPrendaByTipo("Pantalon", setPantalones);
    getPrendaByTipo("Calzados", setCalzado);
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
