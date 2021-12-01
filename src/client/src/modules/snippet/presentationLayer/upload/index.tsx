import React from "react";
import {cardContainer} from "../../../auth/presentationLayer/login/style";
import NexusCard from "../../../core/components/nexusCard";
import {Button, Grid, TextField} from "@mui/material";
import {useNavigate, useParams} from "react-router-dom";
import snippetService from "../../serviceLayer/snippetService";
import {Snippet} from "../../interface/snippetSearch/SnippetSearchResponse";

interface Props {
    [name: string]: any
}

interface State {
    description: string,
    tags: string,
    file: File | undefined,
    showError: boolean
    errorMessage: string,
    [name: string]: any
}

class SnippetUpload extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);

        this.state = {
            description: "",
            tags: "",
            file: undefined,
            showError: false,
            errorMessage: ""
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.updateState = this.updateState.bind(this);
        this.handleFileUpload = this.handleFileUpload.bind(this);
    }

    updateState(obj: any) {
        this.setState({
            ...this.state,
            ...obj
        })
    }

    handleSubmit(event: React.SyntheticEvent) {
        event.preventDefault();
        console.log("Submit called")
        console.log(JSON.stringify(this.state))
        if (this.state.file === undefined) {
            this.updateState({
                showError: true,
                errorMessage: "Choose file to upload"
            })
            console.log("File cannot be empty")
            return
        }
        snippetService.uploadSnippet(this.state.description, this.state.tags, this.state.file)
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
    handleChange(event: React.SyntheticEvent) {
        const { name, value } = event.target as HTMLButtonElement;
        // console.log("Value:", value);
        this.updateState({
            [name]: value
        })
    }

    handleFileUpload(event: React.ChangeEvent<HTMLInputElement>) {
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
            <div style={cardContainer}>
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
                                    Upload
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
            </div>
        );
    }
}

const SnippetUploadView = (props: any) => {
    let navigate = useNavigate();
    let params = useParams();
    return <SnippetUpload navigate={navigate} params={params} {...props}/>
}

export default SnippetUploadView;