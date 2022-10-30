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
import { legalTerms } from "../assets/properties";
import TermsAndConditions from "../assets/tyc.png"
import { useState } from "react";

export default function LegalTerms({setButtonState}) {
  const [isCheckAccepted, setIsAccepted] = useState(false);
  const [isCheckNotAccepted, setIsNotAccepted] = useState(false);

  const handleClickAccepted = () => {
    localStorage.setItem("terminos","True");
    setIsAccepted(true);
    setIsNotAccepted(false);
    setButtonState(false)
    
  };
  const handleClickNotAccepted = () => {
    localStorage.setItem("terminos","False");
    setIsAccepted(false);
    setIsNotAccepted(true);
    setButtonState(false)
  };

  return (
      <div style={{padding:'5px'}}>
        <Typography gutterBottom variant="h5">
          Términos y Condiciones de Dressy
        </Typography>
        <Typography variant="body2">{legalTerms}</Typography>
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
              label="Acepto"
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
              label="No acepto"
            />
          </FormGroup>
        </CardActions>
        </div>
  );
}
