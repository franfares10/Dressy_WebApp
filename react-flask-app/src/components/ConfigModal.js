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
import { Link } from "react-router-dom";
import "./ConfigModal.css";
import postTermsAndGender from "../controllers/SliderController";

const stepperOptions = ["Términos y condiciones", "Elegir género"];

export default function ConfigModal() {
  const [openModal, setOpenModal] = useState(false);
  const [countStep, setCountStep] = useState(0);
  const [buttonState,setButtonState] = useState(true)

  const handlePlusStep = async () => {
    setCountStep((prevCountStep) => prevCountStep + 1);

    if (countStep === 1) {
      //Cierra el handle cuando termina el stepper.
      handleClose();
    }
  };

  const handleMinusStep = async () => {
    setCountStep((prevCountStep) => prevCountStep - 1);
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
    width: "60%",
    height: "40%",
    bgcolor: "background.white",
    boxShadow: 24,
    p: 4,
  };

  return (
    <div>
      <Button
        className="botonIrProbador"
        style={{ backgroundColor: "#545fef" }}
        variant="contained"
        onClick={(e) => {
          e.preventDefault();
          setOpenModal(true);
        }}
      >
        Ir al Probador
      </Button>

      <Modal
        open={openModal}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box style={style}>
          <div
            style={{
              backgroundColor: "white",
              padding: "5px",
              borderRadius: "10px",
            }}
          >
            <Stepper activeStep={countStep} orientation="vertical">
              <Step key={stepperOptions[0]}>
                <StepLabel>{stepperOptions[0]}</StepLabel>
                <StepContent>
                  <LegalTerms setButtonState={setButtonState}/>
                  <Button
                    style={{ float: "right", marginRight: "5px" }}
                    variant="contained"
                    color="primary"
                    disabled={buttonState}
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
                  <div
                    style={{
                      display: "inline-block",
                      float: "right",
                      marginRight: "20px",
                      marginTop: "10px",
                      marginBottom: "10px",
                    }}
                  >
                    <Button
                      variant="contained"
                      color="error"
                      style={{ marginRight: "15px" }}
                      onClick={()=>{handleMinusStep();setButtonState(true)}}
                    >
                      Volver
                    </Button>
                    <Link to={"/home"}>
                      <Button variant="contained" color="primary" onClick={(e)=>{postTermsAndGender()}}>
                        Continuar
                      </Button>
                    </Link>
                  </div>
                </StepContent>
              </Step>
            </Stepper>
          </div>
        </Box>
      </Modal>
    </div>
  );
}
