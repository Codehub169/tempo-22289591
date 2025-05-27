from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import logging

# Import actual functions for resume parsing and portfolio generation
from core.resume_parser import parse_resume
from core.portfolio_generator import generate_portfolio_html

app = Flask(__name__, static_folder='../../frontend/build', static_url_path='/')
CORS(app) # Enable CORS for all routes

# Configure logging
if not app.debug:
    # In production, you might want to configure more robust logging
    # For now, basic logging to stderr
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)

# --- Configuration for file uploads ---
# Define the path for temporarily storing uploaded resumes
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    try:
        os.makedirs(UPLOAD_FOLDER)
        app.logger.info(f"Created upload folder: {UPLOAD_FOLDER}")
    except OSError as e:
        app.logger.error(f"Error creating upload folder {UPLOAD_FOLDER}: {e}")
        # Depending on the severity, you might want to exit or raise an exception

# Allowed resume file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload_resume', methods=['POST'])
def upload_resume_route():
    """API endpoint to upload a resume file and get portfolio data/HTML."""
    if 'resume' not in request.files:
        app.logger.warning("Upload attempt with no 'resume' file part in request")
        return jsonify({'error': 'No resume file part in the request'}), 400
    
    file = request.files['resume']
    
    if file.filename == '':
        app.logger.warning("Upload attempt with no selected file (empty filename)")
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not filename: # secure_filename might return an empty string for dangerous filenames
            app.logger.warning(f"Upload attempt with an invalid/unsafe filename: {file.filename}")
            return jsonify({'error': 'Invalid filename'}), 400
            
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(file_path)
            app.logger.info(f"File {filename} saved to {file_path}")
        except Exception as e:
            app.logger.exception(f"Error saving uploaded file {filename}: {e}")
            return jsonify({'error': f'Error saving file: {str(e)}'}), 500
        
        try:
            # Actual parsing and generation logic
            parsed_data = parse_resume(file_path)
            if parsed_data.get("error"):
                app.logger.error(f"Error parsing resume {filename}: {parsed_data['error']}")
                return jsonify({'error': f'Error processing file: {parsed_data["error"]}"}), 500

            portfolio_html = generate_portfolio_html(parsed_data)
            if "Error: Could not generate portfolio" in portfolio_html: # Check for known error string from generator
                 app.logger.error(f"Error generating portfolio HTML for {filename}: Template issue or rendering failed.")
                 return jsonify({'error': 'Failed to generate portfolio display from parsed data.'}), 500

            app.logger.info(f"Successfully processed resume {filename}")
            return jsonify({
                'message': 'Resume uploaded and processed successfully.',
                'html_content': portfolio_html, 
                'extracted_data': parsed_data
            }), 200
        except Exception as e:
            app.logger.exception(f"Critical error processing file {filename} after saving: {e}")
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
        finally:
            # Clean up the uploaded file if desired, or keep for debugging.
            # For now, we keep it. Consider a cleanup strategy for production.
            # For example, a periodic task to remove old files.
            # if os.path.exists(file_path):
            #     try:
            #         os.remove(file_path)
            #         app.logger.info(f"Cleaned up uploaded file: {file_path}")
            #     except OSError as e:
            #         app.logger.error(f"Error removing uploaded file {file_path}: {e}")
            pass
            
    app.logger.warning(f"Upload attempt with disallowed file type: {file.filename}")
    return jsonify({'error': 'File type not allowed. Please upload PDF or DOCX.'}), 400

# --- Serve React App ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    """Serves the main index.html for the React app and its static assets."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    elif path == "favicon.ico": 
        favicon_path = os.path.join(app.static_folder, 'favicon.ico')
        if os.path.exists(favicon_path):
            return send_from_directory(app.static_folder, 'favicon.ico')
        else:
            # Silently ignore or return a default favicon if preferred over 404
            app.logger.debug("Favicon.ico not found in static folder.")
            abort(404) 
    else:
        # Serve index.html for any route not matching a static file (client-side routing)
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # The port is set to 9000 as per requirements.
    # Host '0.0.0.0' makes it accessible from any network interface.
    # debug=True is suitable for development. Ensure it's False in production if not using a production WSGI server.
    app.run(host='0.0.0.0', port=9000, debug=True)
