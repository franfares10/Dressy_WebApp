import {
  Box,
  Button,
  Modal,
  Step,
  StepContent,
  StepLabel,
  Stepper,
} from "@mui/material";
import { useState } from "react";
import GenderCard from "./GenderCard";
import LegalTerms from "./LegalTerms";

const stepperOptions = [
  "Aceptar términos y condiciones de Dressy",
  "Elegir género",
];

export default function ConfigModal() {
  const [openModal, setOpenModal] = useState(false);
  const [countStep, setCountStep] = useState(0);

  const handlePlusStep = async () => {
    setCountStep((prevCountStep) => prevCountStep + 1);

    if (countStep === 1) {
      //Cierra el handle cuando termina el stepper.
      handleClose();
    }
  };

  const handleClose = () => {
    setOpenModal(false);
    setCountStep(0);
  };

  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 900,
    height: 400,
    bgcolor: "background.white",
    boxShadow: 24,
    p: 4,
  };

  return (
    <div>
      <Button
        variant="contained"
        color="secondary"
        onClick={(e) => {
          e.preventDefault();
          setOpenModal(true);
        }}
      >
        Comenzar la experiencia!
      </Button>

      <Modal
        open={openModal}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box style={style}>
          <div style={{ backgroundColor: "white" }}>
            <Stepper activeStep={countStep} orientation="vertical">
              <Step key={stepperOptions[0]}>
                <StepLabel>{stepperOptions[0]}</StepLabel>
                <StepContent>
                  <LegalTerms />
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={(e) => {
                      e.preventDefault();
                      handlePlusStep();
                    }}
                  >
                    Continuar
                  </Button>
                </StepContent>
              </Step>
              <Step key={stepperOptions[1]}>
                <StepLabel>{stepperOptions[1]}</StepLabel>
                <StepContent>
                  <GenderCard />
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={(e) => {
                      e.preventDefault();
                      handlePlusStep();
                    }}
                  >
                    Continuar
                  </Button>
                </StepContent>
              </Step>
            </Stepper>
          </div>
        </Box>
      </Modal>
    </div>
  );
}
