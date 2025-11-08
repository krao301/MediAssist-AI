import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './routes/Home';
import Incident from './routes/Incident';
import Contacts from './routes/Contacts';
import Summary from './routes/Summary';
import './styles/index.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/incident/:incidentId" element={<Incident />} />
        <Route path="/contacts" element={<Contacts />} />
        <Route path="/summary/:incidentId" element={<Summary />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
