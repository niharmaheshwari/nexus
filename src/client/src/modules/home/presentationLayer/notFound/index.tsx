import React from 'react'
import {home} from "./style";
import NexusCard from "../../../core/components/nexusCard";
class NotFound extends React.Component {
  render(){
    return (
        <div style={home}>
          <NexusCard>
            <h1> 404 Page Not Found</h1>
          </NexusCard>
        </div>
    );
  }
}

export default NotFound;