import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AuthRouter from './modules/auth/router';
import Home from './modules/home/presentationLayer/landing';
import NotFound from './modules/home/presentationLayer/notFound';


const AppRouter = () => (
  <Router>
    <Routes>
      <Route path="auth/*" element={<AuthRouter/>}/>
      <Route path="/" element={<Home/>}/>
      <Route path="*" element={<NotFound/>}/>
    </Routes>
  </Router>
);

export default AppRouter;
