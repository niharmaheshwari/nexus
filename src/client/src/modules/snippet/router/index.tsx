import {Route, Routes} from "react-router-dom";
import SnippetSearch from "../presentationLayer/search";
import PrivateRoute from "../../user/serviceLayer/privateRoute";
import NotFound from "../../home/presentationLayer/notFound";

const SnippetRouter = () => (
    <Routes>
        <Route path='/' element={<PrivateRoute/>}>
            <Route path='/' element={<SnippetSearch/>}/>
        </Route>
        <Route path="*" element={<NotFound/>}/>
    </Routes>
);

export default SnippetRouter;