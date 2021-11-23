import {home} from "./style";
import NexusCard from "../../../core/components/nexusCard";
import React from "react";
import {useNavigate, useParams} from "react-router-dom";
import {Button, Grid, TextField} from "@mui/material";


const DashboardView = (props: any) => {
    let navigate = useNavigate();

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