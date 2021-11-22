import React from 'react';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './modules/auth/presentationLayer/login'
import SignUp from './modules/auth/presentationLayer/signUp';
import AuthRouter from './modules/auth/router';


const AppRouter = () => (
  <Router>
    <Routes>
      <Route path="auth/*" element={<AuthRouter/>}/>
    </Routes>
  </Router>
);

export default AppRouter;
