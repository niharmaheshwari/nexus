import { Grid } from "@mui/material";
import { NavBarButton, LogoButton } from "./components";
import "./style.css"

const TopNavBar = () => {
    return (
        <div className="navbar-container">
            <Grid container spacing={2} justifyContent="space-around">
                <Grid item xs={4}>
                    <div style={{display: "flex", justifyContent: "flex-start"}}>
                        <LogoButton destination={"/"} style={{padding: "5px"}}>NEXUS</LogoButton>
                    </div>
                </Grid>
                <Grid item xs={8}>
                    <div style={{display: "flex", justifyContent: "flex-end"}}>
                        <NavBarButton destination={"/auth/login"} style={{padding: "5px"}}>Login</NavBarButton>
                        <NavBarButton destination={"/auth/sign-up"} style={{padding: "5px"}}>Sign Up</NavBarButton>
                        <NavBarButton destination={"/dashboard"} style={{padding: "5px"}}>Dashboard</NavBarButton>
                    </div>
                </Grid>
            </Grid>
        </div>
    );
};

export default TopNavBar;