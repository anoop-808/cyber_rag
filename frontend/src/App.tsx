import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SearchPage from './pages/SearchPage';
import Home from './pages/Home';
import CVEDetail from './pages/CVEDetail';
import Ask from './pages/Ask';
import { ToastProvider } from './components/ui/Toast';
import './styles/App.css';

function App() {
    return (
        <div className="App">
            <ToastProvider>
                <BrowserRouter>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/search" element={<SearchPage />} />
                        <Route path="/cve/:id" element={<CVEDetail />} />
                        <Route path="/ask" element={<Ask />} />
                    </Routes>
                </BrowserRouter>
            </ToastProvider>
        </div>
    );
}

export default App;
