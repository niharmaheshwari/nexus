import {useLocation, useNavigate} from "react-router-dom";
import {Snippet} from "../../interface/snippetSearch/SnippetSearchResponse";

const SnippetUpdateView = () => {
    let location = useLocation();
    let navigate = useNavigate();
    const snippet: Snippet = location.state
    console.log("Recived snippet", JSON.stringify(location.state))
    return (
        <p>Snippet Update View</p>
    );
}

export default SnippetUpdateView;