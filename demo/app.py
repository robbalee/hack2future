"""
Insurance Claims Fraud Prediction Demo - Flask Application

This is a simple Flask web application that serves a frontend demo
for insurance claims fraud prediction.

To run this application:
1. Make sure you have Flask installed: pip install flask
2. Run the application: python app.py
3. Open your browser and navigate to: http://localhost:5000

The application will serve the main page with a form for entering
claim details and display simulated fraud prediction results.
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import uuid
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our new services and models
from models import Claim, FileInfo
from services import HybridDataService
from utils import ValidationError, Config


def create_app(testing=False):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Initialize services
    data_service = HybridDataService()
    config = Config()
    
    # Store data_service in app context for testing
    app.data_service = data_service

    # Configuration for file uploads
    UPLOAD_FOLDER = config.get('app.upload_folder', 'uploads')
    MAX_FILE_SIZE = config.get('app.max_file_size', 16 * 1024 * 1024)  # 16MB max file size
    ALLOWED_EXTENSIONS = config.get('app.allowed_extensions', {'pdf', 'png', 'jpg', 'jpeg', 'gif'})

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
    app.config['TESTING'] = testing

    # Create uploads directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'pdfs'), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'images'), exist_ok=True)

    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def save_uploaded_file(file, file_type, claim_id):
        """
        Save an uploaded file and return file information.
        """
        if file and allowed_file(file.filename):
            # Get file extension
            original_filename = file.filename
            file_extension = original_filename.rsplit('.', 1)[1].lower()
            
            # Generate unique filename with claim ID
            unique_filename = f"{claim_id}_{uuid.uuid4().hex}.{file_extension}"
            
            # Determine subfolder based on file type
            subfolder = 'pdfs' if file_type == 'pdf' else 'images'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], subfolder, unique_filename)
            
            # Save the file
            file.save(filepath)
            
            return {
                'original_name': original_filename,
                'saved_name': unique_filename,
                'file_path': filepath,
                'file_type': file_type,
                'file_size': os.path.getsize(filepath)
            }
        return None

    @app.route('/')
    def index():
        """
        Main route that serves the index.html template.
        This displays the insurance claims fraud prediction demo form.
        """
        return render_template('index.html')

    @app.route('/admin')
    def admin():
        """
        Admin dashboard to view submitted claims.
        """
        return render_template('admin.html')

    @app.route('/submit_claim', methods=['POST'])
    def submit_claim():
        """
        Handle claim submission with file uploads.
        Saves uploaded files and returns file information.
        """
        try:
            # Get form data
            claim_id = request.form.get('claimId', str(uuid.uuid4()))
            claim_amount = request.form.get('claimAmount')
            description = request.form.get('description')
            
            # Validate required fields
            if not claim_amount or not description:
                return jsonify({'success': False, 'error': 'Missing required fields'}), 400
            
            uploaded_files = []
            
            # Handle PDF document upload
            if 'pdfDocument' in request.files:
                pdf_file = request.files['pdfDocument']
                if pdf_file.filename:
                    file_info = save_uploaded_file(pdf_file, 'pdf', claim_id)
                    if file_info:
                        uploaded_files.append(file_info)
            
            # Handle image evidence uploads
            if 'imageEvidence' in request.files:
                image_files = request.files.getlist('imageEvidence')
                for image_file in image_files:
                    if image_file.filename:
                        file_info = save_uploaded_file(image_file, 'image', claim_id)
                        if file_info:
                            uploaded_files.append(file_info)
            
            # Save claim data to using our data service
            claim_data = {
                'claim_id': claim_id,
                'claim_amount': float(claim_amount),
                'description': description,
                'uploaded_files': uploaded_files,
                'submission_time': datetime.now().isoformat()
            }
            
            # Save the claim using our data service
            try:
                saved_claim_id = data_service.save_claim(claim_data)
                return jsonify({
                    'success': True, 
                    'uploadedFiles': uploaded_files,
                    'message': f'Claim {saved_claim_id} submitted successfully',
                    'claim_id': saved_claim_id
                })
            except ValidationError as e:
                return jsonify({'success': False, 'error': e.message, 'validation_errors': e.errors}), 400
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/get_claim/<claim_id>')
    def get_claim(claim_id):
        """
        Retrieve claim data and file information by claim ID.
        """
        try:
            # Get claim using data service
            claim = data_service.get_claim(claim_id)
            
            if not claim:
                return jsonify({'success': False, 'error': 'Claim not found'}), 404
            
            return jsonify({
                'success': True,
                'claim': claim
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/download_file/<claim_id>/<filename>')
    def download_file(claim_id, filename):
        """
        Download uploaded files by claim ID and filename.
        """
        try:
            # Check if file is PDF or image based on extension
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension == 'pdf':
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'pdfs', filename)
            else:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'images', filename)
            
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
            else:
                return jsonify({'success': False, 'error': 'File not found'})
                
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/list_claims')
    def list_claims():
        """
        List all submitted claims.
        """
        try:
            # Get limit and offset from query parameters
            limit = int(request.args.get('limit', 100))
            offset = int(request.args.get('offset', 0))
            
            # Get claims using data service
            claims = data_service.list_claims(limit=limit)
            
            # Apply offset manually if needed
            if offset > 0 and offset < len(claims):
                claims = claims[offset:]
            
            # Format for response
            claim_list = []
            for claim in claims:
                # Handle both object and dictionary formats
                if isinstance(claim, dict):
                    claim_list.append({
                        'claim_id': claim.get('claim_id'),
                        'claim_amount': claim.get('claim_amount'),
                        'submission_time': claim.get('submission_time'),
                        'files_count': len(claim.get('uploaded_files', [])),
                        'status': claim.get('status'),
                        'fraud_score': claim.get('fraud_score')
                    })
                else:
                    # For object type (when using local service)
                    claim_list.append({
                        'claim_id': claim.claim_id,
                        'claim_amount': claim.claim_amount,
                        'submission_time': claim.submission_time,
                        'files_count': len(claim.uploaded_files),
                        'status': claim.status,
                        'fraud_score': claim.fraud_score
                    })
            
            return jsonify({'success': True, 'claims': claim_list})
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/update_claim/<claim_id>', methods=['POST'])
    def update_claim(claim_id):
        """
        Update an existing claim.
        """
        try:
            # Get JSON data from request
            update_data = request.get_json()
            
            if not update_data:
                return jsonify({'success': False, 'error': 'No update data provided'}), 400
            
            # Update claim using data service
            updated_claim = data_service.update_claim(claim_id, update_data)
            
            if not updated_claim:
                return jsonify({'success': False, 'error': 'Claim not found or update failed'}), 404
            
            # Handle both dict and object return types
            if isinstance(updated_claim, dict):
                claim_data = updated_claim
            else:
                claim_data = updated_claim.to_dict()
                
            return jsonify({
                'success': True,
                'claim': claim_data,
                'message': f'Claim {claim_id} updated successfully'
            })
            
        except ValidationError as e:
            return jsonify({'success': False, 'error': e.message, 'validation_errors': e.errors}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/events/<entity_id>')
    def get_events(entity_id):
        """
        Get events for a specific entity (e.g., a claim)
        """
        try:
            # Get limit from query parameters
            limit = int(request.args.get('limit', 100))
            
            # Get events using the hybrid data service
            events = data_service.list_events(entity_id, limit)
            
            return jsonify({
                'success': True,
                'events': events,
                'count': len(events)
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    return app


# Create the app for running the script directly
app = create_app()

if __name__ == '__main__':
    # Run the Flask application
    # Use Azure's PORT environment variable or default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print("Starting Insurance Claims Fraud Prediction Demo...")
    if debug_mode:
        print("Open your browser and navigate to: http://localhost:5000")
    else:
        print(f"Production server starting on port {port}")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
