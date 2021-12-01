import {useLocation, useNavigate, useParams} from "react-router-dom";
import {Snippet} from "../../interface/snippetSearch/SnippetSearchResponse";
import React from "react";
import {home} from "../../../dashboard/presentationLayer/dashboard/style";
import NexusCard from "../../../core/components/nexusCard";
import {Button, Grid, TextField} from "@mui/material";
import snippetService from "../../serviceLayer/snippetService";

interface Props {
    [name: string]: any
}

interface State {
    description: string,
    tags: string,
    file: File | undefined,
    shareList: string,
    showError: boolean
    errorMessage: string,
    [name: string]: any
}

class SnippetUpdate extends React.Component<Props, State> {
    private snippet: Snippet
    constructor(props: Props) {
        super(props);

        this.snippet = props.location.state;
        this.state = {
            description: this.snippet.desc,
            tags: this.snippet.tags !== null ? this.snippet.tags.join(',') : "",
            shareList: this.snippet.shares !== null ? this.snippet.shares.join(',') : "",
            file: undefined,
            showError: false,
            errorMessage: ""
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.updateState = this.updateState.bind(this);
        this.handleFileUpload = this.handleFileUpload.bind(this);
    }

    handleSubmit(event: React.SyntheticEvent) {
        event.preventDefault();
        console.log("Submit called")
        console.log(JSON.stringify(this.state))
        snippetService.updateSnippet(this.snippet.id, this.state.description, this.state.tags, this.state.shareList, this.state.file)
            .then((response) => {
                const snippet: Snippet = response.data?.data
                this.props.navigate("/snippet/" + snippet.id, {state: snippet});
            })
            .catch((error) => {
                this.updateState({
                    showError: true,
                    errorMessage: "Unable to upload file"
                })
                console.log("Unable to upload file", JSON.stringify(error))
            })
    }
    handleChange(event: React.SyntheticEvent){
        const { name, value } = event.target as HTMLButtonElement;
        // console.log("Value:", value);
        this.updateState({
            [name]: value
        })
    }
    updateState(obj: any) {
        this.setState({
            ...this.state,
            ...obj
        })
    }
    handleFileUpload(event: React.ChangeEvent<HTMLInputElement>){
        if (!event.target.files) {
            return;
        }
        const uploadedFile = event.target.files[0];
        console.log("Files:", uploadedFile);
        this.updateState({
            file: uploadedFile
        })
    }


    render() {
        return (
            <div style={home}>
                <NexusCard>
                    <Grid style={{paddingTop: "10px", paddingBottom: "10px"}} container alignItems="flex-start" direction="row" justifyContent="space-between" spacing={2}>
                        <Grid item xs={4}>
                            <h3>Description</h3>
                            <p>{this.snippet.desc}</p>
                            <h3>Language</h3>
                            <p>{this.snippet.lang}</p>
                            <h3>Author</h3>
                            <p>{this.snippet.author}</p>
                            <h3>Snippet URL</h3>
                            <a href={this.snippet.uri} target = "_blank" >Click here to view the snippet</a>
                            <h3>Tags</h3>
                            <ul>
                                {
                                    this.snippet.tags.map((item, idx) => {
                                        return <li key={idx+item}>{item}</li>
                                    })
                                }
                            </ul>
                            <h3>Shared With</h3>
                            {this.snippet.shares !== null && this.snippet.shares.length !== 0
                                ? <>
                                    <ul>
                                        {
                                            this.snippet.tags.map((item, idx) => {
                                                return <li key={idx+item}>{item}</li>
                                            })
                                        }
                                    </ul>
                                </>
                                : <p>This snippet is not shared with anybody</p>
                            }
                        </Grid>
                        <Grid item xs={8}>
                            <NexusCard>
                                <form onSubmit={this.handleSubmit}>
                                    <Grid style={{paddingTop: "10px", paddingBottom: "10px"}} container alignItems="center" direction="column" justifyContent="center" spacing={2}>
                                        <Grid item>
                                            <TextField
                                                id="description-input"
                                                name="description"
                                                label="Description"
                                                type="text"
                                                size="small"
                                                value={this.state.description}
                                                onChange={this.handleChange}
                                            />
                                        </Grid>
                                        <Grid item>
                                            <TextField
                                                id="tags-input"
                                                name="tags"
                                                label="Tags ',' seperated"
                                                type="text"
                                                size="small"
                                                value={this.state.tags}
                                                onChange={this.handleChange}
                                            />
                                        </Grid>
                                        <Grid item>
                                            <TextField
                                                id="shareList-input"
                                                name="shareList"
                                                label="Share List ',' seperated"
                                                type="text"
                                                size="small"
                                                value={this.state.shareList}
                                                onChange={this.handleChange}
                                            />
                                        </Grid>
                                        <Grid item>
                                            <TextField
                                                id="file-input"
                                                name="file"
                                                type="file"
                                                size="small"
                                                value={this.state.snippetFile}
                                                onChange={this.handleFileUpload}
                                            />
                                        </Grid>
                                        <Grid item>
                                            <Button variant="contained" color="primary" type="submit">
                                                Update
                                            </Button>
                                        </Grid>
                                        {this.state.showError
                                            ? <Grid item>
                                                <p style={{color: "red"}}>{this.state.errorMessage}</p>
                                            </Grid>
                                            : <></>
                                        }
                                    </Grid>
                                </form>
                            </NexusCard>
                        </Grid>
                    </Grid>
                </NexusCard>
            </div>
        );
    }
}

const SnippetUpdateView = (props: any) => {
    let location = useLocation();
    let navigate = useNavigate();
    let params = useParams();
    return <SnippetUpdate  navigate={navigate} params={params} location={location} {...props}/>
}

export default SnippetUpdateView;