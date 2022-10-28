import React, { useRef, useState } from "react";
import { Swiper, SwiperSlide } from "swiper/react";
// Import Swiper styles
import "swiper/css";
import "swiper/css/pagination";
import "./swiper.css";
import history from "../../utils/history";
// import required modules
import { Pagination } from "swiper";
import Visualizacion from "../../views/visualizacion";
import { Routes, Route, Link, Router, BrowserRouter } from "react-router-dom";

const Slider = (prendas, tipo) => {
  return (
    <div className="container">
      <h2>{prendas.tipo}</h2>
      <Swiper
        slidesPerView={3}
        spaceBetween={30}
        pagination={{
          clickable: true,
        }}
        modules={[Pagination]}
        className="swiper"
      >
        {prendas.prendas.map((prenda, index) => {
          return (
            <SwiperSlide key={index} className="swiper-slide">
              <div className="image-container">
<<<<<<< HEAD
                <Link  to={"/visualizacion"} state={[prenda,1]} >
                <img className="prenda" src={prenda.img_url} alt={prenda.descripcion} />
                <p className="product-description">{prenda.descripcion}</p>
                <p className="product-price">{prenda.precio}$</p>
                <div className="brand-container">
                  <img className="brand" src={prenda.marca.url_marca}/>
                </div>
=======
                <Link to={"/visualizacion"} state={[prenda, 1]}>
                  <img
                    className="prenda"
                    src={prenda.img_url}
                    alt={prenda.descripcion}
                  />

                  <p className="product-description">{prenda.descripcion}</p>

                  <p className="product-price">{prenda.precio}$</p>

                  <div className="brand-container">
                    <img className="brand" src={prenda.marca.url_marca} />
                  </div>
>>>>>>> fe3ca3dee46e79839442e25eece924bb96ae26d0
                </Link>
              </div>
            </SwiperSlide>
          );
        })}
      </Swiper>
    </div>
  );
};

export default Slider;
