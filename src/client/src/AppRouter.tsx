import React from 'react';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './modules/auth/presentationLayer/login'
import SignUp from './modules/auth/presentationLayer/signUp';


const AppRouter = () => (
  <Router>
    <Routes>
      <Route path="/login" element={<Login/>}></Route>
      <Route path="/sign-up" element={<SignUp/>}></Route>
    </Routes>
  </Router>
);

export default AppRouter;
