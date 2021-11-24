import {Route, Routes} from "react-router-dom";
import SnippetSearchView from "../presentationLayer/search";
import PrivateRoute from "../../user/serviceLayer/privateRoute";
import NotFound from "../../home/presentationLayer/notFound";
import SnippetDetailView from "../presentationLayer/detail";

const SnippetRouter = () => (
    <Routes>
        <Route path='/' element={<PrivateRoute/>}>
            <Route path='/' element={<SnippetSearchView/>}/>
            <Route path='/:id' element={<SnippetDetailView/>}/>
        </Route>
        <Route path="*" element={<NotFound/>}/>
    </Routes>
);

export default SnippetRouter;