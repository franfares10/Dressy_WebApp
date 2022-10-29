import MenIcon from "../assets/menIcon.png";
import WomenIcon from "../assets/womenIcon.png";
import {
  Card,
  CardActions,
  CardContent,
  CardMedia,
  Checkbox,
  FormControl,
  FormControlLabel,
  FormGroup,
  Typography,
} from "@mui/material";
import { useState } from "react";

export default function GenderCard() {
  const saveToLocalStorage = (gender) => {
    localStorage.setItem("genero", gender);
  };

  const [isCheckAccepted, setIsAccepted] = useState(false);
  const [isCheckNotAccepted, setIsNotAccepted] = useState(false);
  const [otherGender, setOtherGender] = useState(false);

  const handleClickAccepted = () => {
    setIsAccepted(true);
    setIsNotAccepted(false);
    setOtherGender(false)
    saveToLocalStorage("hombre")
    
  };
  const handleClickNotAccepted = () => {
    setIsAccepted(false);
    setIsNotAccepted(true);
    setOtherGender(false)
    saveToLocalStorage("mujer")
  };
  const handleClickNotAcceptedOtherGender = () => {
    setIsAccepted(false);
    setIsNotAccepted(false);
    setOtherGender(true)
    localStorage.removeItem("genero")
  };
  return (
    <div style={{padding:'5px'}}>
        <Typography variant="h3">Elija su género</Typography>
        <Typography variant="body2">
          Clickee el género con el que se identifique, en caso de que no desee hacerlo, o no se sienta identificado con ninguna opción, pulse
          continuar. En caso de no haber elegido, no se aplicará el filtro por
          género a las prendas.
        </Typography>
        <CardActions>
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox
                  checked={isCheckAccepted}
                  onClick={(e) => {
                    handleClickAccepted();
                  }}
                />
              }
              label="Hombre"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={isCheckNotAccepted}
                  onClick={(e) => {
                    handleClickNotAccepted();
                  }}
                />
              }
              label="Mujer"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={otherGender}
                  onClick={(e) => {
                    handleClickNotAcceptedOtherGender();
                  }}
                />
              }
              label="Otro/Prefiero no decirlo"
            />
          </FormGroup>
        </CardActions>
        </div>
  );
}
