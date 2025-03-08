import { useState } from 'react';
import axios from 'axios';

const Sidebar = ({ isOpen, onProcessingComplete }) => {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError("Please select a PDF file");
      return;
    }
    
    if (file.type !== 'application/pdf') {
      setError("Only PDF files are allowed");
      return;
    }
    
    const formData = new FormData();
    formData.append('cv_file', file);
    
    setIsUploading(true);
    setError(null);
    
    try {
      const response = await axios.post('/api/process-cv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      onProcessingComplete(response.data);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to process CV");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <div className="sidebar-header">
        <h5>Upload Your CV</h5>
      </div>
      
      <div className="sidebar-content">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="cv-file" className="form-label">Select PDF file</label>
            <input 
              type="file" 
              className="form-control" 
              id="cv-file" 
              onChange={handleFileChange}
              accept=".pdf"
            />
          </div>
          
          <button 
            type="submit" 
            className="btn btn-primary w-100"
            disabled={!file || isUploading}
          >
            {isUploading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Processing...
              </>
            ) : "Upload and Process CV"}
          </button>
        </form>
        
        {error && (
          <div className="alert alert-danger mt-3">
            {error}
          </div>
        )}
      </div>
      
      <style jsx>{`
        .sidebar {
          position: absolute;
          top: 0;
          left: -300px;
          width: 300px;
          height: 100%;
          background-color: #f8f9fa;
          border-right: 1px solid #dee2e6;
          transition: left 0.3s ease;
          z-index: 1000;
          overflow-y: auto;
          padding: 20px;
        }
        
        .sidebar.open {
          left: 0;
        }
        
        .sidebar-header {
          margin-bottom: 20px;
          padding-bottom: 10px;
          border-bottom: 1px solid #dee2e6;
        }
        
        .sidebar-content {
          display: flex;
          flex-direction: column;
        }
        
        @media (max-width: 768px) {
          .sidebar {
            width: 100%;
          }
        }
      `}</style>
    </div>
  );
};

export default Sidebar;