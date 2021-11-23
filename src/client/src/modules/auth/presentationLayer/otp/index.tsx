import React from "react";
import {cardContainer} from "../signUp/style";
import NexusCard from "../../../core/components/nexusCard";
import {Button, Grid, TextField} from "@mui/material";

interface Props {
    [name: string]: any
}

interface State {
    otp: string
}

class OTPView extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);

        this.state = {
            otp: ""
        }

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleSubmit(event: React.SyntheticEvent) {
        event.preventDefault();
        console.log("Submit called")
        console.log(JSON.stringify(this.state))
    }

    handleChange(event: React.SyntheticEvent) {
        const { name, value } = event.target as HTMLButtonElement;
        this.setState({
            ...this.state,
            [name]: value,
        });
    }

    render() {
        return (
            <div style={cardContainer}>
                <NexusCard>
                    <form onSubmit={this.handleSubmit}>
                        <Grid style={{paddingTop: "10px", paddingBottom: "10px"}} container alignItems="center" direction="column" justifyContent="center" spacing={2}>
                            <Grid item>
                                <TextField
                                    id="otp-input"
                                    name="otp"
                                    label="OTP"
                                    type="text"
                                    size="small"
                                    value={this.state.otp}
                                    onChange={this.handleChange}
                                />
                            </Grid>
                            <Grid item>
                                <Button variant="contained" color="primary" type="submit">
                                    Submit OTP
                                </Button>
                            </Grid>
                        </Grid>
                    </form>
                </NexusCard>
            </div>
        );
    }
}

export default OTPView;