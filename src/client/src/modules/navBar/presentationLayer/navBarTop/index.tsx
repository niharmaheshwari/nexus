import { Grid } from "@mui/material";

const TopNavBar = () => {
    return (
        <Grid container spacing={2} justifyContent="space-around">
            <Grid item xs={4}>
                <div>NEXUS</div>
            </Grid>
            <Grid container item xs={8}>
                <Grid item xs={4}>
                    <div>Login</div>
                </Grid>
                <Grid item xs={4}>
                    <div>Sign Up</div>
                </Grid>
                <Grid item xs={4}>
                    <div>Dashboard</div>
                </Grid>
            </Grid>
        </Grid>
    );
};

export default TopNavBar;