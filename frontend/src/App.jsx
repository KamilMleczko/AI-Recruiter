import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import PdfSummarization from './pages/PdfSummarization';
import JobsMatched from './pages/JobsMatched';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [processingResult, setProcessingResult] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleProcessingResult = (result) => {
    setProcessingResult(result);
    setSidebarOpen(false); 
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <Router>
      <div className="app-container">
        <Navbar toggleSidebar={toggleSidebar} />
        
        <div className="content-container">
          <Sidebar 
            isOpen={sidebarOpen} 
            onProcessingComplete={handleProcessingResult} 
          />
           <main className={`main-content ${sidebarOpen ? 'shifted' : ''}`}>
            <Routes>
              <Route 
                path="/" 
                element={<PdfSummarization data={processingResult} />} 
              />
              <Route 
                path="/job-match/1" 
                element={<JobsMatched data={processingResult} matchIndex={0} />} 
              />
              <Route 
                path="/job-match/2" 
                element={<JobsMatched data={processingResult} matchIndex={1} />} 
              />
              <Route 
                path="/job-match/3" 
                element={<JobsMatched data={processingResult} matchIndex={2} />} 
              />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;