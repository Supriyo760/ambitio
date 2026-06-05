import { Routes, Route } from 'react-router-dom';
import { AppShell } from './components/AppShell';
import { MatterWorkspace } from './pages/MatterWorkspace';
import { DocumentsPage } from './pages/DocumentsPage';

import { ExtractedFactsPage } from './pages/ExtractedFactsPage';
import { EvidencePage } from './pages/EvidencePage';
import { DraftPage } from './pages/DraftPage';
import { LearningPage } from './pages/LearningPage';
import { DocumentReviewPage } from './pages/DocumentReviewPage';
import { EvaluationPage } from './pages/EvaluationPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<AppShell />}>
        <Route index element={<MatterWorkspace />} />
        <Route path="documents" element={<DocumentsPage />} />
        <Route path="review" element={<DocumentReviewPage />} />
        <Route path="facts" element={<ExtractedFactsPage />} />
        <Route path="evidence" element={<EvidencePage />} />
        <Route path="draft" element={<DraftPage />} />
        <Route path="learning" element={<LearningPage />} />
        <Route path="evaluation" element={<EvaluationPage />} />
      </Route>
    </Routes>
  );
}

export default App;
