import React from "react";
import {Routes, Route, Navigate} from "react-router-dom";
import Login from "../components/pages/Login";
import Form from "../components/pages/Form";
import AboutUs from "../components/pages/AboutUs";
import SignUp from "../components/pages/SignUp";
import RegisterCompanies from "../components/pages/RegisterCompanies";


export const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/login" element={<Login/>} />
            <Route path="/form" element={<Form />} />
            <Route path="/" element={<AboutUs />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/RegisterCompanies" element={<RegisterCompanies />} />

        </Routes>
    );
}

export default AppRoutes;