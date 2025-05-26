/**
 * Insurance Claims Fraud Prediction Demo - JavaScript Logic
 * 
 * This script handles the form submission and simulates fraud prediction
 * results using random data and simple rules.
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('claimForm');
    const submitBtn = document.getElementById('submitBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const predictionResult = document.getElementById('predictionResult');
    
    // Form submission handler
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent default form submission
        
        // Get form data
        const formData = {
            claimId: document.getElementById('claimId').value,
            claimAmount: parseFloat(document.getElementById('claimAmount').value),
            description: document.getElementById('description').value
        };
        
        // Validate form data
        if (!validateForm(formData)) {
            return;
        }
        
        // Show loading indicator
        showLoading();
        
        // Simulate API call delay
        setTimeout(() => {
            const prediction = generateFraudPrediction(formData);
            displayPredictionResult(prediction, formData);
            hideLoading();
        }, 2000); // 2 second delay for realism
    });
    
    /**
     * Validates the form data
     */
    function validateForm(data) {
        if (!data.claimId || !data.claimAmount || !data.description) {
            alert('Please fill in all required fields.');
            return false;
        }
        
        if (data.claimAmount <= 0) {
            alert('Claim amount must be greater than 0.');
            return false;
        }
        
        return true;
    }
    
    /**
     * Shows the loading indicator
     */
    function showLoading() {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Analyzing...';
        loadingIndicator.classList.remove('hidden');
        predictionResult.classList.add('hidden');
    }
    
    /**
     * Hides the loading indicator
     */
    function hideLoading() {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Claim for Analysis';
        loadingIndicator.classList.add('hidden');
    }
    
    /**
     * Generates a simulated fraud prediction based on claim data
     */
    function generateFraudPrediction(claimData) {
        let fraudScore = Math.floor(Math.random() * 81) + 10; // Random score between 10-90
        let fraudLikelihood = 'Low';
        
        // Apply simple rules to bias the prediction
        
        // Rule 1: High claim amounts are more suspicious
        if (claimData.claimAmount > 10000) {
            fraudScore += Math.floor(Math.random() * 20) + 10; // Add 10-30 points
        }
        
        // Rule 2: Car insurance specific factors
        // Since this is for car insurance, we can add car-specific risk factors
        if (claimData.claimAmount > 25000) {
            fraudScore += Math.floor(Math.random() * 15) + 10; // High-value auto claims are more suspicious
        }
        
        // Rule 3: Very short descriptions might be suspicious
        if (claimData.description.length < 20) {
            fraudScore += Math.floor(Math.random() * 15) + 5; // Add 5-20 points
        }
        
        // Rule 4: Car insurance specific keywords in description
        const suspiciousKeywords = ['urgent', 'emergency', 'immediate', 'cash', 'total loss', 'stolen', 'hit and run', 'no fault'];
        const descriptionLower = claimData.description.toLowerCase();
        const keywordMatches = suspiciousKeywords.filter(keyword => 
            descriptionLower.includes(keyword)
        ).length;
        
        if (keywordMatches > 0) {
            fraudScore += keywordMatches * 8; // Add 8 points per suspicious keyword
        }
        
        // Ensure score stays within bounds
        fraudScore = Math.min(95, Math.max(5, fraudScore));
        
        // Determine likelihood based on score
        if (fraudScore >= 70) {
            fraudLikelihood = 'High';
        } else if (fraudScore >= 40) {
            fraudLikelihood = 'Medium';
        } else {
            fraudLikelihood = 'Low';
        }
        
        return {
            score: fraudScore,
            likelihood: fraudLikelihood,
            factors: generateAnalysisFactors(claimData, fraudScore)
        };
    }
    
    /**
     * Generates analysis factors based on claim data
     */
    function generateAnalysisFactors(claimData, score) {
        const factors = [];
        
        if (claimData.claimAmount > 25000) {
            factors.push(`High auto claim amount ($${claimData.claimAmount.toLocaleString()}) increases risk assessment`);
        }
        
        if (claimData.description.length < 20) {
            factors.push('Brief description may indicate insufficient detail');
        }
        
        // Add auto insurance specific factors
        factors.push('Auto insurance claim analysis completed');
        
        // Add some random factors for variety
        const randomFactors = [
            'Vehicle damage assessment patterns analyzed',
            'Accident location and timing reviewed',
            'Claimant driving history appears consistent',
            'Documentation requirements met',
            'Geographic risk factors for auto claims considered',
            'Traffic pattern analysis completed'
        ];
        
        const numRandomFactors = Math.floor(Math.random() * 3) + 1;
        for (let i = 0; i < numRandomFactors; i++) {
            const randomIndex = Math.floor(Math.random() * randomFactors.length);
            factors.push(randomFactors[randomIndex]);
            randomFactors.splice(randomIndex, 1); // Remove to avoid duplicates
        }
        
        return factors;
    }
    
    /**
     * Displays the prediction result on the page
     */
    function displayPredictionResult(prediction, claimData) {
        // Set fraud likelihood with appropriate styling
        const likelihoodElement = document.getElementById('fraudLikelihood');
        likelihoodElement.textContent = prediction.likelihood;
        
        // Apply color styling based on likelihood
        likelihoodElement.className = 'px-3 py-1 rounded-full text-sm font-semibold ';
        switch (prediction.likelihood) {
            case 'Low':
                likelihoodElement.className += 'bg-green-100 text-green-800';
                break;
            case 'Medium':
                likelihoodElement.className += 'bg-yellow-100 text-yellow-800';
                break;
            case 'High':
                likelihoodElement.className += 'bg-red-100 text-red-800';
                break;
        }
        
        // Set fraud score
        document.getElementById('fraudScore').textContent = `${prediction.score}%`;
        
        // Update progress bar
        const scoreBar = document.getElementById('fraudScoreBar');
        scoreBar.style.width = `${prediction.score}%`;
        
        // Color the progress bar based on score
        if (prediction.score >= 70) {
            scoreBar.className = 'h-2 rounded-full transition-all duration-500 ease-out bg-red-500';
        } else if (prediction.score >= 40) {
            scoreBar.className = 'h-2 rounded-full transition-all duration-500 ease-out bg-yellow-500';
        } else {
            scoreBar.className = 'h-2 rounded-full transition-all duration-500 ease-out bg-green-500';
        }
        
        // Generate analysis text
        const analysisText = `
            Analysis of auto insurance claim ${claimData.claimId} for $${claimData.claimAmount.toLocaleString()}:
            ${prediction.factors.join('. ')}. 
            Based on these factors, the system has assigned a fraud score of ${prediction.score}% 
            with a ${prediction.likelihood.toLowerCase()} likelihood of fraudulent activity.
        `;
        
        document.getElementById('analysisText').textContent = analysisText;
        
        // Show the result
        predictionResult.classList.remove('hidden');
        
        // Scroll to result
        predictionResult.scrollIntoView({ behavior: 'smooth' });
    }
});
