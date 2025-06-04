import React from "react";
import {Routes, Route, Navigate} from "react-router-dom";
import Login from "../components/pages/Login";
import Form from "../components/pages/Form";
import AboutUs from "../components/pages/AboutUs";
import SignUp from "../components/pages/SignUp";

export const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<Login/>} />
            <Route path="/form" element={<Form />} />
            <Route path="/about-us" element={<AboutUs />} />
            <Route path="/signup" element={<SignUp />} />
        </Routes>
    );
}

export default AppRoutes;