import { Route, Routes } from 'react-router-dom';
import LoginView from '../presentationLayer/login';
import SignUpView from '../presentationLayer/signUp';
import NotFound from "../../home/presentationLayer/notFound";
import OTPView from "../presentationLayer/otp";

const AuthRouter = () => (
        <Routes>
            <Route path="/login" element={<LoginView/>}/>
            <Route path="/sign-up" element={<SignUpView/>}/>
            <Route path="/otp" element={<OTPView/>}/>
            <Route path="*" element={<NotFound/>}/>
        </Routes>
);

export default AuthRouter;