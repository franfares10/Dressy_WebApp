import Slider from "./Slider2/Slider";
import logo from "../assets/logo2.png";
import { Pagination, Navigation, Autoplay } from "swiper";
import { Swiper, SwiperSlide } from "swiper/react";
import Pagina1 from "../assets/Pagina6.png";
import Pagina2 from "../assets/Pagina5.png";
import Pagina3 from "../assets/Pagina4.png";
import "swiper/css/autoplay";
import "./AutoSlider.css";
import { Button, Paper } from "@mui/material";
import { Link } from "react-router-dom";
import ConfigModal from "./ConfigModal";
import { useState } from "react";


export default function AutoSlider() {
  const imagenesAyuda = [
    { descripcion: "¿Qué es Dressy?", url_marca: Pagina1 },
    { descripcion: "¿Cómo funciona Dressy?", url_marca: Pagina2 },
    { descripcion: "¿En qué me beneficia Dressy?", url_marca: Pagina3 },
  ];
  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  return (
    <div className="containerSwiperModal">
      <img src={logo} className='logo' />
      <div className="swiperSpace">
        <Swiper
          className="swiper"
          slidesPerView={1}
          spaceBetween={30}
          autoplay={{ delay: 3000 }}
          modules={[Pagination, Navigation, Autoplay]}
          onAutoplay={(e)=>{document.querySelector(".swiper-slide-active").style.background = '#FFFFFF00'}}
          onAfterInit={(e)=>{document.querySelector(".swiper-slide-active").style.background = '#FFFFFF00'}}
        >
          {imagenesAyuda.map((imagen, index) => {
            return (
              <SwiperSlide
                key={index}
                className="swiper-slide"
              >
                <div className="image-container">
                  <img
                    className="image"
                    src={imagen.url_marca}
                    alt={imagen.descripcion}
                  />
                </div>
              </SwiperSlide>
            );
          })}
        </Swiper>
      </div>
      <div className="button-container">
        <ConfigModal />
      </div>
    </div>
  );
}

const swiperStyle = {
  "swiper-slide": {
    "text-align": "center",
    "font-size": "18px",
    background: "#ffffff",
    display: "-webkit-box",
    display: "-ms-flexbox",
    display: "-webkit-flex",
    display: "flex",
    "-webkit-box-pack": "center",
    "-ms-flex-pack": "center",
    "-webkit-justify-content": "center",
    "justify-content": "center",
    "-webkit-box-align": "center",
    "-ms-flex-align": "center",
    "-webkit-align-items": "center",
    "align-items": "center",
    "border-radius": "15px",
    position: "relative",
    "text-shadow": "1px 1px 2px black",
  },
};
