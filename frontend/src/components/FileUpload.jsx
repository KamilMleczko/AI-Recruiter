import { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState(null);
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
    setResult(null);
    setError(null);
    
    try {
      const response = await axios.post('/api/process-cv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to process CV");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="cv-upload-container">
      <h2>Upload Your CV</h2>
      <form onSubmit={handleSubmit}>
        <div className="file-input-container">
          <input 
            type="file" 
            onChange={handleFileChange} 
            id="cv-file"
            accept=".pdf" 
          />
          <label htmlFor="cv-file">
            {file ? file.name : "Choose PDF file"}
          </label>
        </div>
        
        <button 
          type="submit" 
          disabled={!file || isUploading}
        >
          {isUploading ? "Processing..." : "Upload and Process CV"}
        </button>
      </form>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      {result && (
        <div className="result-container">
          <h3>Processing Result</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default FileUpload;