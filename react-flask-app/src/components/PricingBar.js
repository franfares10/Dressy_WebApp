import { Card, CardContent, Divider } from "@mui/material";
import CheckroomIcon from '@mui/icons-material/Checkroom';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
export default function PrincingBar({ropa,precio}){
    return(
        <Card style={{height:"100px",width:"auto"}}>
            <CardContent>
                <div style={{display:"flex",alignItems:"flex-start"}}>
                    <CheckroomIcon/>
                    {ropa}
                </div>
                <Divider/>
                <div style={{display:"flex"}}>
                    <AttachMoneyIcon/>
                    {precio}
                </div>
            </CardContent>
        </Card>
    )
}