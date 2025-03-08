import ReactMarkdown from 'react-markdown';

const JobMatch = ({ data, matchIndex }) => {
  const hasData = data && 
                data.jobs_matched && 
                data.jobs_matched[matchIndex] &&
                data.evaluation && 
                data.evaluation[matchIndex];
  
  const jobMatch = hasData ? data.jobs_matched[matchIndex] : '';
  const evaluation = hasData ? data.evaluation[matchIndex] : '';
  
  return (
    <div className="container">
      <h1>Job Match {matchIndex + 1}</h1>
      
      {hasData ? (
        <div className="job-match-container">
          <div className="markdown-content mb-5">
            <h2>Job Details</h2>
            <ReactMarkdown>{jobMatch}</ReactMarkdown>
          </div>
          
          <div className="markdown-content">
            <h2>Candidate Evaluation</h2>
            <ReactMarkdown>{evaluation}</ReactMarkdown>
          </div>
        </div>
      ) : (
        <div className="empty-state">
          <div className="icon">💼</div>
          <h3>No Job Match Available</h3>
          <p>Upload a CV using the "Upload CV" button to see job matches and evaluations.</p>
        </div>
      )}
    </div>
  );
};

export default JobMatch;