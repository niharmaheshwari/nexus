import React from "react";
import {ButtonProps as Props} from "../../../interface/navBarTop";
import {Button} from "@mui/material";
import {Link} from "react-router-dom";

const LogoButton = (props: Props) => {
    return (
        <div style={props.style}>
            <Button color="secondary"
                    component={Link}
                    to={props.destination}>{props.children}</Button>
        </div>
    );
};

export default LogoButton;