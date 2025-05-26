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

from flask import Flask, render_template

# Create Flask application instance
app = Flask(__name__)

@app.route('/')
def index():
    """
    Main route that serves the index.html template.
    This displays the insurance claims fraud prediction demo form.
    """
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask application
    # debug=True enables auto-reload when files change during development
    print("Starting Insurance Claims Fraud Prediction Demo...")
    print("Open your browser and navigate to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
