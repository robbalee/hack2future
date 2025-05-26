# Car Insurance Claims Fraud Prediction Demo

A modern, responsive web application that demonstrates a simulated car insurance claims fraud prediction system. Built with Flask (Python) backend and vanilla JavaScript frontend using Tailwind CSS for styling. Includes file upload functionality for PDF documents and image evidence.

## Features

- **Modern Dark UI**: Clean, responsive dark theme design using Tailwind CSS
- **Interactive Form**: Input fields for claim details (ID, amount, description)
- **File Uploads**: Support for PDF documents and image evidence
- **Persistent Storage**: Claims and files are saved to the backend
- **Admin Dashboard**: View and manage submitted claims
- **Simulated ML Prediction**: Mock fraud detection with scoring algorithm
- **Visual Feedback**: Color-coded risk levels and animated progress bars
- **Real-time Analysis**: Simulated processing with loading indicators

## Project Structure

```
demo/
├── app.py                 # Flask application with file upload handling
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   ├── index.html        # Main claim submission form
│   └── admin.html        # Admin dashboard for viewing claims
├── static/
│   └── script.js         # JavaScript logic with file upload support
├── uploads/              # Directory for uploaded files
│   ├── pdfs/            # PDF documents
│   └── images/          # Image evidence
└── claims_data/         # JSON files storing claim information
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the demo directory:**
   ```bash
   cd demo
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install Flask directly:
   ```bash
   pip install flask
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   - Main form: Navigate to `http://localhost:5000`
   - Admin dashboard: Navigate to `http://localhost:5000/admin`

## Usage

### Submitting a Claim

1. **Fill out the claim form:**
   - Enter a Claim ID (e.g., "CLM-2025-001")
   - Specify the claim amount in dollars
   - Provide a brief description of the claim

2. **Upload supporting documents (optional):**
   - **PDF Document**: Upload insurance documents, police reports, or other PDFs
   - **Image Evidence**: Upload photos of damage, accident scenes, or other visual evidence (multiple files allowed)

3. **Submit for analysis:**
   - Click "Submit Claim for Analysis"
   - Files will be uploaded and saved to the backend
   - Wait for the simulated processing (2 seconds)

4. **View results:**
   - See the fraud likelihood (Low/Medium/High)
   - Review the fraud score percentage
   - Read the detailed analysis summary

### Admin Dashboard

1. **Access the admin panel:**
   - Navigate to `http://localhost:5000/admin`
   - View all submitted claims in a table format

2. **Manage claims:**
   - Click "View Details" to see full claim information
   - Download uploaded files directly from the interface
   - See file counts and submission timestamps

## How the Fraud Prediction Works

The demo uses a simple rule-based system to simulate fraud detection:

- **Claim Amount**: Higher amounts (>$25,000) increase fraud risk for auto claims
- **Description Length**: Very brief descriptions may indicate suspicion
- **Keywords**: Car insurance specific words trigger additional risk points
- **File Uploads**: Presence of supporting documentation affects fraud scoring
- **Base Randomization**: Ensures varied results for demonstration

## Technical Details

### Backend (Flask)

- **File Upload Handling**: Secure file upload with validation
- **Persistent Storage**: Claims saved as JSON files, uploaded files organized by type
- **RESTful API**: Endpoints for submitting claims, retrieving data, and downloading files
- **Admin Interface**: Dashboard for viewing and managing submitted claims
- **Development server**: Auto-reload enabled for development

### Frontend (HTML/CSS/JS)

- **HTML**: Semantic structure with accessibility features and file upload inputs
- **CSS**: Tailwind CSS for utility-first styling with dark theme
- **JavaScript**: Vanilla JS for form handling, file uploads, and DOM manipulation

### Styling

- **Responsive Design**: Works on desktop and mobile devices
- **Color Coding**: Green (low risk), yellow (medium risk), red (high risk)
- **Animations**: Smooth transitions and loading indicators
- **Typography**: Modern font choices with proper hierarchy

## API Endpoints

The application provides several API endpoints:

- `POST /submit_claim` - Submit a new claim with file uploads
- `GET /get_claim/<claim_id>` - Retrieve claim data by ID
- `GET /download_file/<claim_id>/<filename>` - Download uploaded files
- `GET /list_claims` - List all submitted claims
- `GET /admin` - Admin dashboard interface

## File Upload Specifications

- **Supported PDF formats**: .pdf
- **Supported image formats**: .png, .jpg, .jpeg, .gif
- **Maximum file size**: 16MB per file
- **Multiple uploads**: Supported for images
- **File organization**: PDFs and images stored in separate directories
- **Unique naming**: Files renamed with claim ID and UUID to prevent conflicts

## Customization

### Modifying Fraud Rules

Edit the `generateFraudPrediction()` function in `static/script.js` to:
- Add new risk factors
- Adjust scoring weights
- Include additional claim types
- Modify suspicious keywords

### Styling Changes

The application uses Tailwind CSS classes. To customize:
- Modify classes in `templates/index.html`
- Extend the Tailwind config in the HTML head
- Add custom CSS if needed

### Adding Features

Potential enhancements:
- Database integration for storing claims
- Real API endpoints for prediction
- User authentication
- Historical claims dashboard
- Export functionality

## Important Notes

⚠️ **Disclaimer**: This is a demonstration application using simulated data. The fraud prediction results are not based on real machine learning models and should not be used for actual insurance decision-making.

## Development

To modify and extend the application:

1. **Backend changes**: Edit `app.py` for routing and Flask configuration
2. **Frontend logic**: Modify `static/script.js` for behavior changes
3. **UI changes**: Update `templates/index.html` for layout modifications

The Flask development server will automatically reload when you make changes to the Python files.

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py` or kill the existing process
2. **Module not found**: Ensure Flask is installed with `pip install flask`
3. **Template not found**: Check that `templates/index.html` exists
4. **Static files not loading**: Verify `static/script.js` exists and Flask static folder is configured

### Browser Console

Check the browser's developer console for any JavaScript errors if the form submission isn't working properly.

## License

This demo is provided for educational and demonstration purposes.
