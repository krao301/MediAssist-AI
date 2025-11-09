import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProtectedRoute } from './components/ProtectedRoute';
import { useApiAuth } from './lib/useApiAuth';
import Home from './routes/Home';
import Incident from './routes/Incident';
import Contacts from './routes/Contacts';
import Summary from './routes/Summary';
import './styles/index.css';

function App() {
  // Setup API authentication with Auth0 tokens
  useApiAuth();

  return (
    <BrowserRouter>
      <ProtectedRoute>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/incident/:incidentId" element={<Incident />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/summary/:incidentId" element={<Summary />} />
        </Routes>
      </ProtectedRoute>
    </BrowserRouter>
  );
}

export default App;
