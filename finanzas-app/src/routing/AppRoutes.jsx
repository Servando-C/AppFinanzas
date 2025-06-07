import React from "react";
import {Routes, Route, Navigate} from "react-router-dom";
import Login from "../components/pages/Login";
import PrivateRoute from '../components/pages/PrivateRoute';
import Dashboard from "../components/pages/Dashboard";
import Form from "../components/pages/Form";
import AboutUs from "../components/pages/AboutUs";
import SignUp from "../components/pages/SignUp";
import RegisterCompanies from "../components/pages/RegisterCompanies";
import Adquisicions from "../components/pages/Adquisicions";
import Addproyects from "../components/pages/Addproyects";
import Admin from "../components/pages/Admin";
import Capturador from "../components/pages/Capturador";
import Reports from "../components/pages/Reports";



export const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route element={<PrivateRoute />}>
                <Route path="/dashboard" element={<Dashboard />} />
            </Route>
            <Route path="/form" element={<Form />} />
            <Route path="/" element={<AboutUs />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/RegisterCompanies" element={<RegisterCompanies/>} />
            <Route path="/Adquisicions" element={<Adquisicions/>} />
            <Route path="/Addproyects" element={<Addproyects/>} />
            <Route path="/Admin" element={<Admin/>} />
            <Route path="/Capturador" element={<Capturador/>} />
            <Route path="/Reports" element={<Reports/>} />



        </Routes>
    );
}

export default AppRoutes;