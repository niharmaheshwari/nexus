import React from 'react'
import {home} from "../../../home/presentationLayer/landing/style";
import NexusCard from "../../../core/components/nexusCard";
class SnippetSearch extends React.Component {
    render(){
        return (
            <div style={home}>
                <NexusCard>
                    <h1> Snippet Search </h1>
                </NexusCard>
            </div>
        );
    }
}

export default SnippetSearch;