import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import SearchPage from './pages/SearchPage';
import Home from './pages/Home';
import CVEDetailPage from './pages/CVEDetailPage';
import './styles/App.css';

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/search" element={<SearchPage />} />
                    <Route path="/cve/:id" element={<CVEDetailPage />} />
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;
