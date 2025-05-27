import React from 'react';

// PortfolioView component: Displays the generated portfolio HTML content.
function PortfolioView({ htmlContent, onClearPortfolio, extractedData }) {

  // The portfolio HTML is directly embedded using an iframe for better isolation 
  // and to handle potential CSS/JS conflicts from the generated content.
  // The `srcDoc` attribute is used to directly provide HTML content to the iframe.

  return (
    <div className="portfolio-view-container">
      <button onClick={onClearPortfolio} className="btn btn-secondary" style={{ marginBottom: '20px' }}>
        Upload New Resume
      </button>
      
      {/* Section to display a summary of extracted data - Optional */} 
      {/* You can expand this section to show more details if needed */}
      {/* For example:
      {extractedData && Object.keys(extractedData).length > 0 && (
        <div style={{ textAlign: 'left', marginBottom: '20px', padding: '15px', background: '#e9ecef', borderRadius: '5px' }}>
          <h4>Quick Summary of Extracted Data:</h4>
          <p><strong>Name:</strong> {extractedData.name || 'N/A'}</p>
          <p><strong>Email:</strong> {extractedData.email || 'N/A'}</p>
          <p><strong>Phone:</strong> {extractedData.phone || 'N/A'}</p>
          {extractedData.skills && <p><strong>Skills Found:</strong> {extractedData.skills.length}</p>}
        </div>
      )} 
      */}

      <div className="portfolio-content">
        {/* Using dangerouslySetInnerHTML as the content is trusted HTML from our backend template */}
        {/* Note: For production, if the HTML can come from arbitrary sources, this is risky. */}
        {/* However, since we control the template, it's acceptable for this use case. */}
        {/* An iframe is a safer alternative for rendering arbitrary HTML. */}
        {/* Let's use an iframe for better isolation and security, as discussed. */}
        <iframe 
          srcDoc={htmlContent} 
          title="Generated Portfolio Preview"
          style={{ width: '100%', height: 'calc(100vh - 180px)', border: '1px solid #ddd', borderRadius: '5px' }}
          sandbox="allow-scripts allow-same-origin" // Sandbox for security, allow scripts if your template needs them.
        />
      </div>
    </div>
  );
}

export default PortfolioView;
