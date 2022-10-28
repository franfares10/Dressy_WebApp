import {
  Card,
  CardActions,
  CardContent,
  CardHeader,
  CardMedia,
  CircularProgress,
  Divider,
  Typography,
} from "@mui/material";
import WorkingManIcon from "../assets/workingPeople.png";
export default function LoadingCard() {
  return (
    <Card>
      <CardContent style={{ textAlign: "center" }}>
        <img src={WorkingManIcon} alt="Esperar" width={250} height={250}></img>
        <Divider />
        <Typography variant="h5">Tu experiencia ya comenzará...</Typography>
        <div style={{paddingTop:"20px"}}>
          <CircularProgress />
        </div>
      </CardContent>
    </Card>
  );
}
