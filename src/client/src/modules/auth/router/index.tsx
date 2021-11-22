import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from '../presentationLayer/login';
import SignUp from '../presentationLayer/signUp';

const AuthRouter = () => (
        <Routes>
            <Route path="/login" element={<Login/>}/>
            <Route path="/sign-up" element={<SignUp/>}/>
        </Routes>
);

export default AuthRouter;