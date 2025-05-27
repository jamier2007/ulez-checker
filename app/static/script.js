// JavaScript for Emission Zone Compliance Checker

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('check-form');
    const registrationInput = document.getElementById('registration');
    const errorMessage = document.getElementById('error-message');
    const loadingElement = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const submitButton = document.getElementById('submit-btn');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Get and validate registration
            const registration = registrationInput.value.trim().toUpperCase().replace(/\s/g, '');
            
            if (!registration) {
                showError('Please enter a registration number');
                return;
            }
            
            if (registration.length < 2 || registration.length > 8) {
                showError('Registration must be between 2-8 characters');
                return;
            }
            
            // Clear previous results and errors
            errorMessage.textContent = '';
            resultContainer.style.display = 'none';
            resultContainer.innerHTML = '';
            
            // Show loading spinner
            loadingElement.style.display = 'block';
            submitButton.disabled = true;
            
            try {
                // Fetch data from API
                const response = await fetch(`/api/${registration}`);
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.detail || 'Error checking compliance');
                }
                
                // Display results
                displayResults(data);
            } catch (error) {
                showError(error.message);
            } finally {
                // Hide loading spinner
                loadingElement.style.display = 'none';
                submitButton.disabled = false;
            }
        });
    }
    
    function showError(message) {
        errorMessage.textContent = message;
        loadingElement.style.display = 'none';
        submitButton.disabled = false;
    }
    
    function displayResults(data) {
        // Create result HTML
        const resultHTML = `
            <div class="result-header ${data.compliant ? 'compliant' : 'non-compliant'}">
                <h2>${data.message || (data.compliant ? 'Your vehicle is compliant.' : 'Your vehicle is not compliant.')}</h2>
                <p class="registration-display">Registration: ${data.registration}</p>
            </div>
            
            <div class="vehicle-details">
                <h3>Vehicle Details</h3>
                <div class="detail-grid">
                    ${data.make_model ? `
                    <div class="detail-item">
                        <span class="detail-label">Make and Model:</span>
                        <span class="detail-value">${data.make_model}</span>
                    </div>
                    ` : ''}
                    
                    ${data.year ? `
                    <div class="detail-item">
                        <span class="detail-label">Year of Registration:</span>
                        <span class="detail-value">${data.year}</span>
                    </div>
                    ` : ''}
                    
                    ${data.engine_category ? `
                    <div class="detail-item">
                        <span class="detail-label">Engine Category:</span>
                        <span class="detail-value">${data.engine_category}</span>
                    </div>
                    ` : ''}
                    
                    ${data.co2_emissions ? `
                    <div class="detail-item">
                        <span class="detail-label">CO2 Emissions:</span>
                        <span class="detail-value">${data.co2_emissions}</span>
                    </div>
                    ` : ''}
                    
                    ${!data.compliant && data.charge ? `
                    <div class="detail-item charge">
                        <span class="detail-label">Daily Charge:</span>
                        <span class="detail-value">£${data.charge}</span>
                    </div>
                    ` : ''}
                </div>
            </div>
            
            <div class="compliance-summary">
                ${data.compliant 
                    ? `<p class="compliant-message">This vehicle meets the emission zone standards and no charge applies.</p>`
                    : `<p class="non-compliant-message">This vehicle does not meet the emission zone standards. ${data.charge ? `A daily charge of £${data.charge} applies when driving in the zone.` : ''}</p>`
                }
            </div>
        `;
        
        // Display results
        resultContainer.innerHTML = resultHTML;
        resultContainer.style.display = 'block';
        
        // Scroll to results
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    }
});
