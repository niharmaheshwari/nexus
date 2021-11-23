import React from 'react'
import {card} from "./style";
import NexusCard from "../../../core/components/nexusCard";
import {Button, Grid, TextField} from "@mui/material";
import SnippetCard from "./components/snippetCard";

interface Props {
    [name: string]: any
}

interface State {
    searchQuery: string
    [name: string]: any
}

class SnippetSearch extends React.Component<Props, State> {

    constructor(props: Props) {
        super(props);

        this.state = {
            searchQuery: "",
        }

        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event: React.SyntheticEvent) {
        const { name, value } = event.target as HTMLButtonElement;
        this.setState({
            ...this.state,
            [name]: value,
        });
    }

    render(){
        return (
            <div style={card}>
                <NexusCard>
                    <h1> Snippet Search </h1>
                    <Grid style={{paddingTop: "10px", paddingBottom: "10px"}} container alignItems="center" direction="row" justifyContent="flex-start" spacing={2}>
                        <Grid item>
                            <TextField
                                id="search-input"
                                name="search"
                                label="Search"
                                type="text"
                                size="small"
                                value={this.state.searchQuery}
                                onChange={this.handleChange}
                            />
                        </Grid>
                        <Grid item>
                            <Button variant="contained" color="primary">
                                Search
                            </Button>
                        </Grid>
                    </Grid>
                    <SnippetCard description={"First snippet"} tags={["tag1", "tag2"]}/>
                </NexusCard>
            </div>
        );
    }
}

export default SnippetSearch;