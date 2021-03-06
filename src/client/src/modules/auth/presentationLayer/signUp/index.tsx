import React from 'react'
import {cardContainer} from "./style";
import NexusCard from "../../../core/components/nexusCard";
import {Button, Grid, TextField} from "@mui/material";
import MomentUtils from "@date-io/moment";
import { MuiPickersUtilsProvider, DatePicker } from '@material-ui/pickers';
import {MaterialUiPickersDate} from "@material-ui/pickers/typings/date";
import signUpService from "../../serviceLayer/signUpService";
import userProfile from "../../../user/serviceLayer/userProfile";
import { useParams, useNavigate } from "react-router-dom";

interface Props {
  [name: string]: any
}

interface State {
  name: string,
  email: string,
  phone: string,
  password: string,
  birthdate: Date | null | undefined,
  validated: boolean,
  validationMessage: string
}
class SignUp extends React.Component<any, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      name: "",
      email: "",
      phone: "",
      password: "",
      birthdate: null,
      validated: true,
      validationMessage: ""
    }
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleDateChange = this.handleDateChange.bind(this);
  }

  handleSubmit(event: React.SyntheticEvent) {
    event.preventDefault();
    console.log("Submit called")
    console.log(JSON.stringify(this.state))
    // this.props.navigate("/auth/otp")
    signUpService.signUp(this.state.name,
        this.state.email,
        this.state.phone,
        this.state.birthdate as Date,
        this.state.password)
        .then((response) => {
          userProfile.updateUserDetails(this.state.name, this.state.email);
          this.props.navigate("/auth/otp")
        })
        .catch((error)=> {
          this.setState({
            ...this.state,
            validated: false,
            validationMessage: error.data?.message
          });
          console.log("API Error message:" + this.state.validationMessage);
          console.log("API Error:" + JSON.stringify(error));
        });
  }

  handleChange(event: React.SyntheticEvent) {
    const { name, value } = event.target as HTMLButtonElement;
    this.setState({
      ...this.state,
      [name]: value,
    });
  }
  handleDateChange(date: MaterialUiPickersDate) {
    console.log(JSON.stringify(date))
    this.setState({
      ...this.state,
      birthdate: date?.toDate(),
    });
  }
  render(){
    return (
        <div style={cardContainer}>
          <NexusCard>
            <form onSubmit={this.handleSubmit}>
              <Grid style={{paddingTop: "10px", paddingBottom: "10px"}} container alignItems="center" direction="column" justifyContent="center" spacing={2}>
                <Grid item>
                  <TextField
                      id="name-input"
                      name="name"
                      label="Name"
                      type="text"
                      size="small"
                      value={this.state.name}
                      onChange={this.handleChange}
                  />
                </Grid>
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
                  <MuiPickersUtilsProvider utils={MomentUtils}>
                    <DatePicker
                        placeholder="Birthdate"
                        format={"MM/DD/YYYY"}
                        value={this.state.birthdate}
                        onChange = {this.handleDateChange}
                        animateYearScrolling={false}
                        autoOk={true}
                        clearable
                    />
                  </MuiPickersUtilsProvider>
                </Grid>
                <Grid item>
                  <TextField
                      id="phone-input"
                      name="phone"
                      label="Phone Number"
                      type="text"
                      size="small"
                      value={this.state.phone}
                      onChange={this.handleChange}
                  />
                </Grid>
                <Grid item>
                  <Button variant="contained" color="primary" type="submit">
                    Sign Up
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

const SignUpView = (props: any) => {
  let navigate = useNavigate();
  let params = useParams();
  return <SignUp navigate={navigate} params={params} {...props}/>
}

export default SignUpView;