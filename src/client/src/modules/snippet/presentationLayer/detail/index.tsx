import {useNavigate, useParams, useLocation} from "react-router-dom";
import {Snippet} from "../../interface/snippetSearch/SnippetSearchResponse";
import {home} from "../../../dashboard/presentationLayer/dashboard/style";
import NexusCard from "../../../core/components/nexusCard";
import {Button, Grid} from "@mui/material";
import snippetService from "../../serviceLayer/snippetService";
import React, {useEffect, useState} from "react";
const SnippetDetailView = (props: any) => {
    let location = useLocation();
    let navigate = useNavigate();
    const snippet: Snippet = location.state
    const [code, setCode] = useState(null);
    const [snippetDeleteFailed, setSnippetDeleteFailed] = useState(false);
    console.log(JSON.stringify("On snippet detail page"));
    useEffect(() => {
        snippetService.fetchSnippet(snippet.uri)
            .then((response) => {
                console.log("Snippet fetched successfully:", JSON.stringify(response.data))
                setCode(response.data)
            })
            .catch((error) => {
                console.log("Snippet fetch failed")
            })
    }, [])
    const handleUpdate = () => {
        navigate("/snippet/update", {state: snippet});
    }
    const handleDelete = () => {
        snippetService.deleteSnippet(snippet.id)
            .then((response) => {
                navigate("/snippet")
            })
            .catch((error) => {
                console.log("Unable to delete snippet:", JSON.stringify(error));
                setSnippetDeleteFailed(true);
            })
    }
    return (
        <div style={home}>
            <NexusCard>
                <Grid style={{paddingTop: "10px", paddingBottom: "10px"}} container alignItems="flex-start" direction="row" justifyContent="space-between" spacing={2}>
                    <Grid item xs={4}>
                        <h3>Description</h3>
                        <p>{snippet.desc}</p>
                        <h3>Language</h3>
                        <p>{snippet.lang}</p>
                        <h3>Author</h3>
                        <p>{snippet.author}</p>
                        <h3>Snippet URL</h3>
                        <a href={snippet.uri} target = "_blank" >Click here to view the snippet</a>
                        <h3>Tags</h3>
                        <ul>
                            {
                                snippet.tags.map((item, idx) => {
                                    return <li key={idx+item}>{item}</li>
                                })
                            }
                        </ul>
                        <h3>Shared With</h3>
                        {snippet.shares !== null && snippet.shares.length !== 0
                            ? <>
                                <ul>
                                    {
                                        snippet.shares.map((item, idx) => {
                                            return <li key={idx+item}>{item}</li>
                                        })
                                    }
                                </ul>
                            </>
                            : <p>This snippet is not shared with anybody</p>
                        }
                        <Grid style={{paddingTop: "10px", paddingBottom: "10px"}} container alignItems="center" direction="row" justifyContent="flex-start" spacing={2}>
                            <Grid item>
                                <Button variant="contained" color="secondary" onClick={handleUpdate}>
                                    UPDATE
                                </Button>
                            </Grid>
                            <Grid item>
                                <Button variant="contained" color="secondary" onClick={handleDelete}>
                                    DELETE
                                </Button>
                            </Grid>
                        </Grid>
                        {snippetDeleteFailed
                            ? <p style={{color: "red"}}>Failed to delete the snippet</p>
                            : <></>
                        }
                    </Grid>
                    <Grid item xs={8}>
                        <pre style={{whiteSpace: "pre-wrap"}}>{code}</pre>
                    </Grid>
                </Grid>
            </NexusCard>
        </div>
    );
}

export default SnippetDetailView