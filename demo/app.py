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

# Create Flask application instance
app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'pdfs'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'images'), exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, file_type, claim_id):
    """Save uploaded file and return file info"""
    if file and allowed_file(file.filename):
        # Create unique filename
        original_filename = file.filename
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{claim_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
        
        # Determine subfolder based on file type
        subfolder = 'pdfs' if file_type == 'pdf' else 'images'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], subfolder, unique_filename)
        
        # Save file
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
        claim_id = request.form.get('claimId')
        claim_amount = request.form.get('claimAmount')
        description = request.form.get('description')
        
        # Validate required fields
        if not claim_id or not claim_amount or not description:
            return jsonify({'success': False, 'error': 'Missing required fields'})
        
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
        
        # Save claim data to JSON file for persistence
        claim_data = {
            'claim_id': claim_id,
            'claim_amount': float(claim_amount),
            'description': description,
            'uploaded_files': uploaded_files,
            'submission_time': datetime.now().isoformat()
        }
        
        # Save to claims directory
        claims_dir = 'claims_data'
        os.makedirs(claims_dir, exist_ok=True)
        
        claim_file_path = os.path.join(claims_dir, f"{claim_id}.json")
        with open(claim_file_path, 'w') as f:
            json.dump(claim_data, f, indent=2)
        
        return jsonify({
            'success': True, 
            'uploadedFiles': uploaded_files,
            'message': f'Claim {claim_id} submitted successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_claim/<claim_id>')
def get_claim(claim_id):
    """
    Retrieve claim data and file information by claim ID.
    """
    try:
        claim_file_path = os.path.join('claims_data', f"{claim_id}.json")
        
        if not os.path.exists(claim_file_path):
            return jsonify({'success': False, 'error': 'Claim not found'})
        
        with open(claim_file_path, 'r') as f:
            claim_data = json.load(f)
        
        return jsonify({'success': True, 'claim_data': claim_data})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

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
        claims_dir = 'claims_data'
        if not os.path.exists(claims_dir):
            return jsonify({'success': True, 'claims': []})
        
        claims = []
        for filename in os.listdir(claims_dir):
            if filename.endswith('.json'):
                with open(os.path.join(claims_dir, filename), 'r') as f:
                    claim_data = json.load(f)
                    claims.append({
                        'claim_id': claim_data['claim_id'],
                        'claim_amount': claim_data['claim_amount'],
                        'submission_time': claim_data['submission_time'],
                        'files_count': len(claim_data['uploaded_files'])
                    })
        
        # Sort by submission time (newest first)
        claims.sort(key=lambda x: x['submission_time'], reverse=True)
        
        return jsonify({'success': True, 'claims': claims})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

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
