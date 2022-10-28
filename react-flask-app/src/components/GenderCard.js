import { Card, CardContent, Typography } from "@mui/material";
import MenIcon from "../assets/menIcon.png";
import WomenIcon from "../assets/womenIcon.png";

export default function GenderCard() {
  const saveToLocalStorage = (gender) => {
    localStorage.setItem("genero", gender);
  };
  return (
    <Card>
      <CardContent>
        <Typography variant="h3">Elija su género</Typography>
        <Typography variant="body2">
          Clickee el género con el que se identifique, en caso de que no desee hacerlo, o no se sienta identificado con ninguna opción, pulse
          continuar. En caso de no haber elegido, no se aplicará el filtro por
          género a las prendas.
        </Typography>
        <div style={{ display:"flex",justifyContent:"space-around",paddingTop:"25px"}}>
          <img
            src={MenIcon}
            width={250}
            height={250}
            alt="hombre"
            onClick={()=>{saveToLocalStorage("hombre")}}
          />
          <img
            src={WomenIcon}
            width={250}
            height={250}
            alt="mujer"
            onClick={()=>{saveToLocalStorage("mujer")}}
          />
        </div>
      </CardContent>
    </Card>
  );
}
