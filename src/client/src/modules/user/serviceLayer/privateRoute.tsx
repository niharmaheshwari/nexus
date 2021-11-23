import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import userProfile from "./userProfile";

const PrivateRoute = () => {
    const auth = userProfile.authenticated

    // If authorized, return an outlet that will render child elements
    // If not, return element that will navigate to login page
    return auth ? <Outlet /> : <Navigate to="/auth/unauthenticated" />;
}

export default PrivateRoute;