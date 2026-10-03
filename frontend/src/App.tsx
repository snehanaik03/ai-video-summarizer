import { Routes, Route } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import LandingPage from './pages/LandingPage';
import HomePage from './pages/HomePage';
import ResultsPage from './pages/ResultsPage';
import NotesPage from './pages/NotesPage';

function App() {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/app" element={<HomePage />} />
        <Route path="/app/results/:id" element={<ResultsPage />} />
        <Route path="/results/:id" element={<ResultsPage />} />
        <Route path="/notes" element={<NotesPage />} />
      </Routes>
    </MainLayout>
  );
}

export default App;
