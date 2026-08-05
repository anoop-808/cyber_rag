import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Search from './pages/Search';
import Ask from './pages/Ask';
import CveDetailRoute from './pages/CveDetail';
import './styles/App.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/ask" element={<Ask />} />
          <Route path="/cve/:id" element={<CveDetailRoute />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
