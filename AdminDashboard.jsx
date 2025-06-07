import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';  // Importamos axios para hacer peticiones HTTP

const AdminDashboard = () => {
    const navigate = useNavigate();
    const [empresas, setEmpresas] = useState([]);
    const [proyectos, setProyectos] = useState([]);
    const [empresaSeleccionada, setEmpresaSeleccionada] = useState(null);

    // Cargar las empresas desde el backend
    useEffect(() => {
        const fetchEmpresas = async () => {
            try {
                const response = await axios.get('/api/empresas');
                // Verifica si la respuesta es un array
                if (Array.isArray(response.data)) {
                    setEmpresas(response.data);
                } else {
                    console.error('La respuesta no es un array:', response.data);
                    setEmpresas([]); // Establece empresas a un array vacío si la respuesta no es válida
                }
            } catch (error) {
                console.error('Error al cargar las empresas:', error);
                setEmpresas([]); // Establece empresas a un array vacío en caso de error
            }
        };

        fetchEmpresas();
    }, []);

    const seleccionarEmpresa = async (empresaId) => {
        setEmpresaSeleccionada(empresaId);

        try {
            // Obtener proyectos de la empresa seleccionada
            const response = await axios.get(`/api/empresas/${empresaId}/proyectos`); // Petición GET con el id de la empresa
            setProyectos(response.data);  // Asumimos que la respuesta es un array de proyectos
        } catch (error) {
            console.error('Error al cargar los proyectos:', error);
        }
    };

    const descargarPDF = (proyectoId) => {
        // Aquí se llamaría al backend para obtener el PDF del balance
        console.log(`Descargando PDF del proyecto ${proyectoId}`);
        // Ejemplo: window.open(`/api/proyectos/${proyectoId}/balance.pdf`, '_blank');
    };

    return (
        <div className="p-6">
            <div className="bg-blue-600 text-white py-4 fixed top-0 w-full z-10 shadow-md">
                <h1 className="text-2xl font-bold text-center">Panel de Administrador</h1>
            </div>

            <div className="mt-16">
                <div className="flex gap-4 mb-6">
                    <button
                        className="bg-blue-600 text-white px-4 py-2 rounded"
                        onClick={() => navigate('/RegisterCompanies')}
                    >
                        Registrar Empresa
                    </button>
                    <button
                        className="bg-green-600 text-white px-4 py-2 rounded"
                        onClick={() => navigate('/RegisterProject')}
                    >
                        Registrar Proyecto
                    </button>
                </div>

                <div className="flex gap-10">
                    <div className="w-1/2">
                        <h2 className="text-xl font-semibold mb-2">Empresas Registradas</h2>
                        <ul className="border rounded p-4">
                            {empresas.map((empresa) => (
                                <li
                                    key={empresa.id}
                                    className={`cursor-pointer p-2 rounded hover:bg-gray-300 ${empresaSeleccionada === empresa.id ? 'bg-gray-100' : ''}`}
                                    onClick={() => seleccionarEmpresa(empresa.id)}
                                    style={{ transition: 'background-color 0.3s ease' }}
                                >
                                    {empresa.nombre}
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="w-1/2">
                        <h2 className="text-xl font-semibold mb-2">Proyectos</h2>
                        {empresaSeleccionada ? (
                            <ul className="border rounded p-4">
                                {proyectos.map((proyecto) => (
                                    <li key={proyecto.id} className="flex justify-between items-center p-2 border-b">
                                        {proyecto.nombre}
                                        <button
                                            className="bg-red-500 text-white px-3 py-1 rounded text-sm"
                                            onClick={() => descargarPDF(proyecto.id)}
                                        >
                                            Descargar Balance PDF
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className="text-gray-500">Selecciona una empresa para ver sus proyectos</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;
