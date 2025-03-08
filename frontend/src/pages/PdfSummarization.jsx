import ReactMarkdown from 'react-markdown';

const PdfSummarization = ({ data }) => {
  const summarization = data?.summarization || '';
  
  return (
    <div className="container">
      <h1>PDF Summarization</h1>
      <div className="pdf-summarization-container">
        {data ? (
            <div className="markdown-content">
            <ReactMarkdown>{summarization}</ReactMarkdown>
            </div>
        ) : (
            <div className="empty-state">
            <div className="icon">📄</div>
            <h3>No CV Processed Yet</h3>
            <p>Upload a CV using the "Upload CV" button to see the summarization.</p>
            </div>
        )}
        </div>
    </div>
  );
};

export default PdfSummarization;