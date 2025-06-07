import React from "react";
import {Routes, Route, Navigate} from "react-router-dom";
import Login from "../components/pages/Login";
import PrivateRoute from '../components/pages/PrivateRoute';
import AdminDashboard from "../components/pages/AdminDashboard";
import Form from "../components/pages/Form";
import AboutUs from "../components/pages/AboutUs";
import SignUp from "../components/pages/SignUp";
import RegisterCompanies from "../components/pages/RegisterCompanies";
import RegisterProject from "../components/pages/RegisterProject";

export const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route element={<PrivateRoute />}>
                <Route path="/AdminDashboard" element={<AdminDashboard />} />
            </Route>
            <Route path="/form" element={<Form />} />
            <Route path="/" element={<AboutUs />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/RegisterCompanies" element={<RegisterCompanies/>} />
            <Route path="/RegisterProject" element={<RegisterProject/>} />
        </Routes>
    );
}

export default AppRoutes;