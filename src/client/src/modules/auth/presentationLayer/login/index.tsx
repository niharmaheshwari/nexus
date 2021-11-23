import React from 'react'
import {cardContainer} from "./style";
import NexusCard from "../../../core/components/nexusCard";
import {Button, Grid, TextField} from "@mui/material";
import userProfile from "../../../user/serviceLayer/userProfile";
import { useParams, useNavigate } from "react-router-dom";

interface Props {
    [name: string]: any
}

interface State {
    email: string,
    password: string,
    [name: string]: any
}


class Login extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);

        this.state = {
            email: "",
            password: "",
            validated: true,
            validationMessage: ""
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
    }

    handleChange(event: React.SyntheticEvent) {
        const { name, value } = event.target as HTMLButtonElement;
        this.updateState({
            [name]: value
        })
    }
    render() {
        return (
            <div style={cardContainer}>
                <NexusCard>
                    <form onSubmit={this.handleSubmit}>
                        <Grid style={{paddingTop: "10px", paddingBottom: "10px"}} container alignItems="center" direction="column" justifyContent="center" spacing={2}>
                            <Grid item>
                                <TextField
                                    id="email-input"
                                    name="email"
                                    label="Email"
                                    type="text"
                                    size="small"
                                    value={this.state.email}
                                    onChange={this.handleChange}
                                />
                            </Grid>
                            <Grid item>
                                <TextField
                                    id="password-input"
                                    name="password"
                                    label="Password"
                                    type="password"
                                    size="small"
                                    value={this.state.password}
                                    onChange={this.handleChange}
                                />
                            </Grid>
                            <Grid item>
                                <Button variant="contained" color="primary" type="submit">
                                    Login
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

const LoginView = (props: any) => {
    let navigate = useNavigate();
    let params = useParams();
    return <Login navigate={navigate} params={params} {...props} />
};

export default LoginView;