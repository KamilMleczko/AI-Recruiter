import { Link, useLocation } from 'react-router-dom';

const Navbar = ({ toggleSidebar }) => {
  const location = useLocation();
  
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container-fluid"> 
            <Link className="navbar-brand" to="/">CV Processor</Link>
            
            <button 
            className="btn btn-outline-light me-2" 
            onClick={toggleSidebar}
            >
            <i className="bi bi-file-earmark-pdf"></i> Upload CV
            </button>

            <button 
            className="navbar-toggler" 
            type="button" 
            data-bs-toggle="collapse" 
            data-bs-target="#navbarNav"
            >
            <span className="navbar-toggler-icon"></span>
            </button>
       
        <div className='space'></div>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link 
                className={`nav-link ${location.pathname === '/' ? 'active' : ''}`} 
                to="/"
              >
                PDF Summarization
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                className={`nav-link ${location.pathname === '/job-match/1' ? 'active' : ''}`} 
                to="/job-match/1"
              >
                Job Match 1
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                className={`nav-link ${location.pathname === '/job-match/2' ? 'active' : ''}`} 
                to="/job-match/2"
              >
                Job Match 2
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                className={`nav-link ${location.pathname === '/job-match/3' ? 'active' : ''}`} 
                to="/job-match/3"
              >
                Job Match 3
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;