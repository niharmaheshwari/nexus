import React from 'react'
import {cardContainer} from "./style";
import NexusCard from "../../../core/components/nexusCard";
import {Grid, TextField} from "@mui/material";

interface Props {
  [name: string]: any
}

interface State {
  name: string,
  email: string,
  phone: string,
  password: string,
  birthdate: string
}
class SignUp extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      name: "",
      email: "",
      phone: "",
      password: "",
      birthdate: ""
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
    // console.log("Name:" + name)
    // console.log("Value:" + value)
    this.setState({
      ...this.state,
      [name]: value,
    });
    // console.log("Change event called")
    console.log(JSON.stringify(this.state))
  }
  render(){
    return (
        <div style={cardContainer}>
          <NexusCard>
            <form onSubmit={this.handleSubmit}>
              <Grid container alignItems="center" direction="column" justifyContent="center" spacing={2}>
                <Grid item>
                  <TextField
                      id="name-input"
                      name="name"
                      label="Name"
                      type="text"
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
                      value={this.state.password}
                      onChange={this.handleChange}
                  />
                </Grid>
              </Grid>
            </form>
          </NexusCard>
        </div>
    );
  }
}

export default SignUp;