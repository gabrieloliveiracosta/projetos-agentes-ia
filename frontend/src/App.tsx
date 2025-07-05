
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import Questionnaire from './pages/Questionnaire';
import InvestorProfile from './pages/InvestorProfile';
import PortfolioResult from './pages/PortfolioResult';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/questionario" element={<Questionnaire />} />
        <Route path="/perfil" element={<InvestorProfile />} />
        <Route path="/carteira" element={<PortfolioResult />} />
      </Routes>
    </Router>
  );
}

export default App;
