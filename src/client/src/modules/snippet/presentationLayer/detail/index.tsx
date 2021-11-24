import {useNavigate, useParams, useLocation} from "react-router-dom";
import {Snippet} from "../../interface/snippetSearch/SnippetSearchResponse";
import {home} from "../../../dashboard/presentationLayer/dashboard/style";
import NexusCard from "../../../core/components/nexusCard";
import {Button, Grid} from "@mui/material";
const SnippetDetailView = (props: any) => {
    let location = useLocation();
    let navigate = useNavigate();
    const snippet: Snippet = location.state
    console.log(JSON.stringify("On snippet detail page"));
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
                                        snippet.tags.map((item, idx) => {
                                            return <li key={idx+item}>{item}</li>
                                        })
                                    }
                                </ul>
                            </>
                            : <p>This snippet is not shared with anybody</p>
                        }
                    </Grid>
                    <Grid item xs={8}>
                        <Button variant="contained" color="primary" onClick={() => navigate("/snippet/upload")}>
                            UPLOAD
                        </Button>
                    </Grid>
                </Grid>
            </NexusCard>
        </div>
    );
}

export default SnippetDetailView