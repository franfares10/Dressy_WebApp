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

export default function LegalTerms() {
  const [isCheckAccepted, setIsAccepted] = useState(false);
  const [isCheckNotAccepted, setIsNotAccepted] = useState(false);

  const handleClickAccepted = () => {
    setIsAccepted(true);
    setIsNotAccepted(false);
    
  };
  const handleClickNotAccepted = () => {
    setIsAccepted(false);
    setIsNotAccepted(true);
  };

  return (
    <Card sx={{ width: "500", height: "500" }}>
      <CardContent>
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
      </CardContent>
    </Card>
  );
}
