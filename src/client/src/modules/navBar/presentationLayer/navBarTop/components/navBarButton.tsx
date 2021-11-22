import React from "react";
import {ButtonProps as Props} from "../../../interface/navBarTop";
import {Button} from "@mui/material";
import {Link} from "react-router-dom";

const NavBarButton = (props: Props) => {
    return (
        <div style={props.style}>
            <Button variant="contained"
                    component={Link}
                    to={props.destination}>{props.children}</Button>
        </div>
    );
};

export default NavBarButton;