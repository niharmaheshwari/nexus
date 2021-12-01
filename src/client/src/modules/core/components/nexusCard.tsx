import React from "react";

interface Props {
    children?: React.ReactNode
    styles?: any
}
const NexusCard = (props: Props) => {
    return (
        <div style={{...cardStyle, ...props.styles}}>
            <div style={containerStyle}>
                {props.children}
            </div>
        </div>
    );
};

const cardStyle = {
    boxShadow: "0 4px 8px 0 rgba(0,0,0,0.2)",
    transition: "0.3s"
};

const containerStyle = {
    padding: "2px 16px"
};

export default NexusCard;