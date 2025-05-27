import axios from 'axios';

// Base URL for the API. Assumes backend is running on port 9000.
// The `proxy` in package.json handles this for development.
const API_BASE_URL = '/api'; // Relative path, proxy will handle it

/**
 * Uploads the resume file to the backend API.
 * @param {FormData} formData - The FormData object containing the resume file.
 * @returns {Promise<Object>} A promise that resolves with the API response (data).
 *                            The response is expected to contain `html_content` and `extracted_data`.
 * @throws {Error} If the API request fails.
 */
export const uploadResume = async (formData) => {
  try {
    // Make a POST request to the /upload_resume endpoint.
    const response = await axios.post(`${API_BASE_URL}/upload_resume`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // Important for file uploads
      },
    });
    // Return the data from the response.
    return response; // Return the whole response so App.js can get status, etc.
  } catch (error) {
    // Log the error for debugging purposes.
    console.error('Error uploading resume:', error.response || error.message);
    // Re-throw the error so it can be caught by the calling component (FileUpload.js).
    throw error;
  }
};

// Potentially, other API service functions could be added here in the future.
// For example: fetchPortfolioTemplates, savePortfolio, etc.
