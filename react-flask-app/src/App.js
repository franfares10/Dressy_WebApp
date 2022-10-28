import React from "react";
import "./App.css";
import { default as ResponsiveAppBar } from "./components/AppBar";
import { Container } from "@mui/system";
import Home from "./views/Home";
import { Routes, Route, Link, Router, BrowserRouter } from "react-router-dom";
import Visualizacion from "./views/visualizacion";
import UnityRenderer from "./views/UnityRenderer";
import AutoSlider from "./components/AutoSlider";

function App() {
  return (
    <div className='app-container'>
      <ResponsiveAppBar />
      <div>
        <Container maxWidth="xl">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/visualizacion" element={<Visualizacion />} />
            <Route path="/unity" element={<UnityRenderer />}></Route>
          </Routes>
        </Container>
      </div>
    </div>
  );
}

export default App;
