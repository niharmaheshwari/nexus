import {useNavigate, useParams, useLocation} from "react-router-dom";
import {Snippet} from "../../interface/snippetSearch/SnippetSearchResponse";
const SnippetDetailView = (props: any) => {
    let location = useLocation();
    const snippet: Snippet = location.state
    console.log(JSON.stringify(snippet));
    return <p>Snippet Detail {snippet.id}</p>
}

export default SnippetDetailView