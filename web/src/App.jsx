import { Routes, Route } from 'react-router-dom';
import Home from './routes/Home';
import Incident from './routes/Incident';
import Contacts from './routes/Contacts';
import Summary from './routes/Summary';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/incident/:incidentId" element={<Incident />} />
      <Route path="/contacts" element={<Contacts />} />
      <Route path="/summary/:incidentId" element={<Summary />} />
    </Routes>
  );
}

export default App;