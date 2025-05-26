# Insurance Claims Fraud Prediction Demo

A modern, responsive web application that demonstrates a simulated insurance claims fraud prediction system. Built with Flask (Python) backend and vanilla JavaScript frontend using Tailwind CSS for styling.

## Features

- **Modern UI**: Clean, responsive design using Tailwind CSS
- **Interactive Form**: Input fields for claim details (ID, amount, type, description)
- **Simulated ML Prediction**: Mock fraud detection with scoring algorithm
- **Visual Feedback**: Color-coded risk levels and animated progress bars
- **Real-time Analysis**: Simulated processing with loading indicators

## Project Structure

```
demo/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    └── script.js         # JavaScript logic
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
   Navigate to `http://localhost:5000`

## Usage

1. **Fill out the claim form:**
   - Enter a Claim ID (e.g., "CLM-2025-001")
   - Specify the claim amount in dollars
   - Select a claim type (Auto, Home, Health, or Life)
   - Provide a brief description of the claim

2. **Submit for analysis:**
   - Click "Submit Claim for Analysis"
   - Wait for the simulated processing (2 seconds)

3. **View results:**
   - See the fraud likelihood (Low/Medium/High)
   - Review the fraud score percentage
   - Read the detailed analysis summary

## How the Fraud Prediction Works

The demo uses a simple rule-based system to simulate fraud detection:

- **Claim Amount**: Higher amounts (>$10,000) increase fraud risk
- **Claim Type**: Different types have varying risk profiles
- **Description Length**: Very brief descriptions may indicate suspicion
- **Keywords**: Certain words trigger additional risk points
- **Base Randomization**: Ensures varied results for demonstration

## Technical Details

### Backend (Flask)

- Serves static files and templates
- Minimal routing with single endpoint
- Development server with auto-reload

### Frontend (HTML/CSS/JS)

- **HTML**: Semantic structure with accessibility features
- **CSS**: Tailwind CSS for utility-first styling
- **JavaScript**: Vanilla JS for form handling and DOM manipulation

### Styling

- **Responsive Design**: Works on desktop and mobile devices
- **Color Coding**: Green (low risk), yellow (medium risk), red (high risk)
- **Animations**: Smooth transitions and loading indicators
- **Typography**: Modern font choices with proper hierarchy

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
