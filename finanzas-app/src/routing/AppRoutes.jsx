import React from "react";
import {Routes, Route, Navigate} from "react-router-dom";
import Login from "../components/pages/Login";

export const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<Login/>} />
        </Routes>
    );
}

export default AppRoutes;