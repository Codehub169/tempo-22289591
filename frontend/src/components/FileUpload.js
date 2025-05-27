import React, { useState } from 'react';
import { uploadResume } from '../services/apiService';

// FileUpload component: Handles the resume file selection and upload process.
function FileUpload({ onUploadSuccess, onUploadError, onSetLoading }) {
  // State to store the currently selected file by the user.
  const [selectedFile, setSelectedFile] = useState(null);
  // State to store any file-specific validation errors (e.g., wrong type).
  const [fileError, setFileError] = useState('');

  // Handles changes to the file input field.
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Basic file type validation.
      if (file.type === 'application/pdf' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        setSelectedFile(file);
        setFileError(''); // Clear any previous file errors.
      } else {
        setSelectedFile(null);
        setFileError('Invalid file type. Please upload a PDF or DOCX file.');
      }
    }
  };

  // Handles the form submission to upload the resume.
  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent default form submission.

    if (!selectedFile) {
      setFileError('Please select a file to upload.');
      return;
    }

    onSetLoading(true); // Signal that loading has started.
    setFileError(''); // Clear previous errors.

    const formData = new FormData();
    formData.append('resume', selectedFile);

    try {
      // Call the API service to upload the resume.
      const response = await uploadResume(formData);
      // On successful upload, call the success callback with the portfolio HTML.
      onUploadSuccess(response.data.html_content, response.data.extracted_data || {}); 
    } catch (error) {
      // On upload failure, call the error callback with a user-friendly message.
      const errorMessage = error.response?.data?.error || error.message || 'An unknown error occurred during upload.';
      onUploadError(errorMessage);
    }
    onSetLoading(false); // Signal that loading has finished.
  };

  return (
    <div className="file-upload-container">
      <h2>Upload Your Resume</h2>
      <p>Upload your resume (PDF or DOCX) to automatically generate your portfolio website.</p>
      <form onSubmit={handleSubmit} className="file-upload-form">
        <div>
          <input 
            type="file" 
            onChange={handleFileChange} 
            accept=".pdf,.docx"
            aria-label="Resume file input"
          />
        </div>
        {/* Display file-specific validation errors here */} 
        {fileError && <p style={{ color: 'red', fontSize: '0.9em', marginTop: '-10px', marginBottom: '10px' }}>{fileError}</p>}
        <button type="submit" className="btn btn-primary" disabled={!selectedFile || fileError}>
          Generate Portfolio
        </button>
      </form>
    </div>
  );
}

export default FileUpload;
