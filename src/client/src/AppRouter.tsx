import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AuthRouter from './modules/auth/router';
import Home from './modules/home/presentationLayer/landing';
import NotFound from './modules/home/presentationLayer/notFound';
import TopNavBar from "./modules/navBar/presentationLayer/navBarTop";
import DashboardView from "./modules/dashboard/presentationLayer/dashboard";
import PrivateRoute from "./modules/user/serviceLayer/privateRoute";


const AppRouter = () => (
  <Router>
     <TopNavBar/>
    <Routes>
        <Route path="auth/*" element={<AuthRouter/>}/>
        <Route path="dashboard" element={<DashboardView/>}/>
        {/*<Route path='dashboard' element={<PrivateRoute/>}>*/}
        {/*    <Route path='dashboard' element={<DashboardView/>}/>*/}
        {/*</Route>*/}
        <Route path="/" element={<Home/>}/>
        <Route path="*" element={<NotFound/>}/>
    </Routes>
  </Router>
);

export default AppRouter;
