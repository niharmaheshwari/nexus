import React from "react";
import {cardContainer} from "../signUp/style";
import NexusCard from "../../../core/components/nexusCard";
import {Button, Grid, TextField} from "@mui/material";
import userProfile from "../../../user/serviceLayer/userProfile";
import otpService from "../../serviceLayer/otpService";
import {useNavigate, useParams} from "react-router-dom";

interface Props {
    [name: string]: any
}

interface State {
    otp: string,
    validated: boolean
    [name: string]: any
}

class OTP extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);

        this.state = {
            otp: "",
            validated: true
        }

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.updateState = this.updateState.bind(this);
    }

    updateState(obj: any) {
        this.setState({
            ...this.state,
            ...obj
        })
    }

    handleSubmit(event: React.SyntheticEvent) {
        event.preventDefault();
        console.log("Submit called")
        console.log(JSON.stringify(this.state))
        if (userProfile.email === undefined) {
            this.updateState({
                validated: false,
                validationMessage: "Email cannot be empty"
            })
            return
        }
        otpService.confirmOtp(userProfile.email, this.state.otp)
            .then((response) => {
                this.props.navigate("/auth/login")
            })
            .catch((error) => {
                console.log("API Error message:" + this.state.validationMessage);
                console.log("API Error:" + JSON.stringify(error));
                this.updateState({
                    validated: false,
                    validationMessage: error.data?.message
                })
            });

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
                            {!this.state.validated
                                ? <Grid item>
                                    <p style={{color: "red"}}>{this.state.validationMessage}</p>
                                </Grid>
                                : <></>
                            }
                        </Grid>
                    </form>
                </NexusCard>
            </div>
        );
    }
}

const OTPView = (props: any) => {
    let navigate = useNavigate();
    let params = useParams();

    return <OTP navigate={navigate} params={params} {...props} />
}

export default OTPView;