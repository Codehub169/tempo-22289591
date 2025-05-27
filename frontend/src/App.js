import React, { useState, useCallback } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import PortfolioView from './components/PortfolioView';

function App() {
  const [portfolioHtml, setPortfolioHtml] = useState(null);
  const [extractedData, setExtractedData] = useState(null); // State for extracted data
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleResumeUploadSuccess = useCallback((html, data) => {
    setPortfolioHtml(html);
    setExtractedData(data); // Store extracted data
    setError('');
    setIsLoading(false);
  }, []);

  const handleUploadError = useCallback((errorMessage) => {
    setError(errorMessage);
    setPortfolioHtml(null);
    setExtractedData(null);
    setIsLoading(false);
  }, []);

  const handleSetLoading = useCallback((loadingStatus) => {
    setIsLoading(loadingStatus);
  }, []);

  const clearPortfolio = () => {
    setPortfolioHtml(null);
    setExtractedData(null);
    setError('');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Resume to Portfolio Generator</h1>
        <p>Upload your resume to instantly generate a professional portfolio website.</p>
      </header>
      <main className="App-main-content">
        {isLoading && (
          <div className="loading-indicator">
            <p>Generating your portfolio, please wait...</p>
            <div className="spinner"></div> 
          </div>
        )}
        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
            <button onClick={() => setError('')} className="btn btn-secondary" style={{marginTop: '10px'}}>Dismiss</button>
          </div>
        )}
        {!isLoading && !portfolioHtml && (
          <FileUpload 
            onUploadSuccess={handleResumeUploadSuccess} 
            onUploadError={handleUploadError} 
            onSetLoading={handleSetLoading} 
          />
        )}
        {!isLoading && portfolioHtml && (
          <PortfolioView 
            htmlContent={portfolioHtml} 
            extractedData={extractedData} // Pass extractedData to PortfolioView
            onClearPortfolio={clearPortfolio} 
          />
        )}
      </main>
      <footer className="App-footer">
        <p>&copy; {new Date().getFullYear()} ResumeSpark. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
