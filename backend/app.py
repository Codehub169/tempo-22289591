from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS
import os

# Import placeholder functions for resume parsing and portfolio generation
# These will be replaced with actual calls to modules in backend.core
# from core.resume_parser import parse_resume
# from core.portfolio_generator import generate_portfolio_html

app = Flask(__name__, static_folder='../../frontend/build', static_url_path='/')
CORS(app) # Enable CORS for all routes

# --- Configuration for file uploads ---
# Define the path for temporarily storing uploaded resumes
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed resume file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload_resume', methods=['POST'])
def upload_resume_route():
    """API endpoint to upload a resume file and get portfolio data/HTML."""
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file part in the request'}), 400
    
    file = request.files['resume']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = file.filename # In a real app, use secure_filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Placeholder for actual parsing and generation logic
            # parsed_data = parse_resume(file_path)
            # portfolio_html = generate_portfolio_html(parsed_data)
            
            # Mock response for now
            parsed_data_mock = {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "123-456-7890",
                "summary": "A highly skilled software engineer...",
                "experience": [
                    {"title": "Senior Developer", "company": "Tech Corp", "years": "2020-Present"}
                ],
                "education": [
                    {"degree": "B.S. Computer Science", "university": "State University", "year": "2019"}
                ],
                "skills": ["Python", "Flask", "React", "JavaScript"]
            }
            # For MVP, we might return JSON data for the frontend to render, 
            # or eventually, the generated HTML or a link to it.
            # For now, returning the extracted (mock) data.
            return jsonify({
                'message': 'Resume uploaded and processed successfully (mock data).',
                'file_path': file_path, # For debugging, remove in prod
                'data': parsed_data_mock
                # 'portfolio_html': portfolio_html # If generating HTML directly
            }), 200
        except Exception as e:
            # Log the exception e
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
        finally:
            # Clean up the uploaded file if desired, or keep for debugging
            # if os.path.exists(file_path):
            #     os.remove(file_path)
            pass
            
    return jsonify({'error': 'File type not allowed'}), 400

# --- Serve React App ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    """Serves the main index.html for the React app and its static assets."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    elif path == "favicon.ico": # Specific handling for favicon if needed
        return send_from_directory(app.static_folder, 'favicon.ico')
    else:
        # Serve index.html for any route not matching a static file (client-side routing)
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # The port is set to 9000 as per requirements.
    # Host '0.0.0.0' makes it accessible from any network interface.
    app.run(host='0.0.0.0', port=9000, debug=True)
