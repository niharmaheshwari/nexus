import {home} from "./style";
import NexusCard from "../../../core/components/nexusCard";
import {Navigate, useNavigate} from "react-router-dom";
import {Button, Grid} from "@mui/material";
import userProfile from "../../../user/serviceLayer/userProfile";


const DashboardView = (props: any) => {
    let navigate = useNavigate();
    if (!userProfile.authenticated) {
        // navigate("/auth/unauthenticated")
        return <Navigate to="/auth/unauthenticated" />;
    }
    return (
        <div style={home}>
            <NexusCard>
                <Grid style={{paddingTop: "10px", paddingBottom: "10px"}} container alignItems="center" direction="row" justifyContent="center" spacing={2}>
                    <Grid item>
                        <Button variant="contained" color="primary" type="submit" onClick={() => navigate("/snippet")}>
                            SEARCH
                        </Button>
                    </Grid>
                    <Grid item>
                        <Button variant="contained" color="primary" onClick={() => navigate("/snippet/upload")}>
                            UPLOAD
                        </Button>
                    </Grid>
                </Grid>
            </NexusCard>
        </div>
    );
};

export default DashboardView;