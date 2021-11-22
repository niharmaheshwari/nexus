import { Grid } from "@mui/material";
import { NavBarButton } from "./components";

const TopNavBar = () => {
    return (
        <Grid container spacing={2} justifyContent="space-around">
            <Grid item xs={4}>
                <div>NEXUS</div>
            </Grid>
            <Grid item xs={8}>
                <div style={{display: "flex", justifyContent: "flex-end"}}>
                    <NavBarButton destination={"/auth/login"} style={{padding: "5px"}}>Login</NavBarButton>
                    <NavBarButton destination={"/auth/sign-up"} style={{padding: "5px"}}>Sign Up</NavBarButton>
                    <NavBarButton destination={"/auth/dashboard"} style={{padding: "5px"}}>Dashboard</NavBarButton>
                </div>
            </Grid>
        </Grid>
    );
};

export default TopNavBar;