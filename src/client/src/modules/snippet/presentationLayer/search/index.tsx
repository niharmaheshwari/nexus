import React from 'react'
import {card} from "./style";
import NexusCard from "../../../core/components/nexusCard";
import {Button, Grid, TextField} from "@mui/material";
import SnippetCard from "./components/snippetCard";
import snippetService from "../../serviceLayer/snippetService";
import {Snippets} from "../../interface/snippetSearch/SnippetSearchResponse";

interface Props {
    [name: string]: any
}

interface State {
    searchQuery: string
    snippets?: Snippets
    [name: string]: any
}

class SnippetSearch extends React.Component<Props, State> {

    constructor(props: Props) {
        super(props);

        this.state = {
            searchQuery: "",
            snippets: undefined
        }

        this.handleChange = this.handleChange.bind(this);
        this.handleSearch = this.handleSearch.bind(this);
        this.updateState = this.updateState.bind(this);
    }

    updateState(obj: any) {
        this.setState({
            ...this.state,
            ...obj
        })
    }

    handleSearch(event: React.SyntheticEvent) {
        event.preventDefault()
        snippetService.search(this.state.searchQuery)
            .then((response) => {
                console.log("Snippets" + JSON.stringify(response.data?.data));
                const snippets: Snippets = response.data?.data
                this.updateState({
                    snippets
                })
            })
            .catch((error) => {
                console.log("API Error:" + JSON.stringify(error));
            })

    }

    handleChange(event: React.SyntheticEvent) {
        const { name, value } = event.target as HTMLButtonElement;
        this.setState({
            ...this.state,
            [name]: value,
        });
    }

    handleSnippetClick(idx: number) {
        if (this.state.snippets === undefined) {
            console.log("No snippets")
            return
        }
        const snippet = this.state.snippets.snippets[idx];
        console.log("Clicked on snippet:" + snippet.id);
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
                                name="searchQuery"
                                label="Search"
                                type="text"
                                size="small"
                                value={this.state.searchQuery}
                                onChange={this.handleChange}
                            />
                        </Grid>
                        <Grid item>
                            <Button variant="contained" color="primary" onClick={this.handleSearch}>
                                Search
                            </Button>
                        </Grid>
                    </Grid>
                    {
                        this.state.snippets?.snippets.map((item, idx) => {
                            return <SnippetCard key={idx}
                                                description={item.desc}
                                                tags={item.tags}
                                                onClick={() => {this.handleSnippetClick(idx)}}/>
                        })
                    }
                    {this.state.snippets !== undefined && this.state.snippets.snippets.length === 0?
                        <p style={{color: "red"}}>No snippets found. Search again</p> :
                        <></>
                    }
                </NexusCard>
            </div>
        );
    }
}

export default SnippetSearch;