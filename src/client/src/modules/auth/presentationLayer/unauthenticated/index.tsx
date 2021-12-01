import React from 'react'
import {home} from "./style";
import NexusCard from "../../../core/components/nexusCard";
class UnauthenticatedView extends React.Component {
    render(){
        return (
            <div style={home}>
                <NexusCard>
                    <h1> User is not logged in</h1>
                </NexusCard>
            </div>
        );
    }
}

export default UnauthenticatedView;