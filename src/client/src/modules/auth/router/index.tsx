import { Route, Routes } from 'react-router-dom';
import Login from '../presentationLayer/login';
import SignUp from '../presentationLayer/signUp';
import NotFound from "../../home/presentationLayer/notFound";

const AuthRouter = () => (
        <Routes>
            <Route path="/login" element={<Login/>}/>
            <Route path="/sign-up" element={<SignUp/>}/>
            <Route path="*" element={<NotFound/>}/>
        </Routes>
);

export default AuthRouter;