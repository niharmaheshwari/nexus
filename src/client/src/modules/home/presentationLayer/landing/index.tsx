import React from 'react'
import NexusCard from "../../../core/components/nexusCard";
import { home } from "./style";

class Home extends React.Component {
  render(){
    return (
      <div style={home}>
        <NexusCard>
          <h3> NEXUS Note Taking App</h3>
            <p>Click one of the links above to continue</p>
        </NexusCard>
      </div>
    );
  }
}

export default Home;