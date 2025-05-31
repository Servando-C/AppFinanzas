import React from "react";
import {Routes, Route, Navigate} from "react-router-dom";
import Login from "../components/pages/Login";
import Form from "../components/pages/Form";

export const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<Login/>} />
            <Route path="/form" element={<Form />} />
        </Routes>
    );
}

export default AppRoutes;