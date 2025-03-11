document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview-image');
    const changeImageBtn = document.getElementById('change-image');
    const analyzeImageBtn = document.getElementById('analyze-image');
    const resultsSection = document.getElementById('results-section');
    const loader = document.getElementById('loader');
    const resultsContainer = document.getElementById('results-container');
    const newAnalysisBtn = document.getElementById('new-analysis');
    
    // Prediction Results Elements
    const resultIcon = document.getElementById('result-icon');
    const predictionText = document.getElementById('prediction-text');
    const confidenceFill = document.getElementById('confidence-fill');
    const confidenceText = document.getElementById('confidence-text');
    const resultMessage = document.getElementById('result-message');
    const symptomsList = document.getElementById('symptoms-list');
    const pesticidesList = document.getElementById('pesticides-list');
    const preventionList = document.getElementById('prevention-list');
    const diseaseInfo = document.getElementById('disease-info');
    const errorInfo = document.getElementById('error-info');
    const errorMessage = document.getElementById('error-message');

    // Event Listeners
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Handle drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileSelection(e.target.files[0]);
        }
    });
    
    changeImageBtn.addEventListener('click', () => {
        resetUI();
    });
    
    analyzeImageBtn.addEventListener('click', () => {
        if (fileInput.files.length) {
            analyzeImage(fileInput.files[0]);
        }
    });
    
    newAnalysisBtn.addEventListener('click', () => {
        resetUI();
        resultsSection.hidden = true;
    });
    
    // Functions
    function handleFileSelection(file) {
        // Check if file is an image
        if (!file.type.match('image/jpeg') && !file.type.match('image/png') && !file.type.match('image/jpg')) {
            showError('Please select a valid image file (JPG, JPEG, or PNG)');
            return;
        }
        
        const reader = new FileReader();
        
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            uploadArea.hidden = true;
            previewContainer.hidden = false;
        };
        
        reader.readAsDataURL(file);
    }
    
    function analyzeImage(file) {
        // Show loading state
        resultsSection.hidden = false;
        loader.hidden = false;
        resultsContainer.hidden = true;
        
        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        
        // Send request to server
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            showError('An error occurred while analyzing the image. Please try again.');
            console.error('Error:', error);
        })
        .finally(() => {
            loader.hidden = true;
            resultsContainer.hidden = false;
        });
    }
    
    function displayResults(data) {
        // Reset previous results
        resetResultsDisplay();
        
        // Check if there was an error
        if (data.error) {
            showError(data.error);
            return;
        }
        
        // Check if image is a grape leaf
        if (!data.is_leaf) {
            showError(data.message || 'The uploaded image does not appear to be a grape leaf.');
            return;
        }
        
        // Handle unrecognized prediction
        if (data.prediction === 'Unrecognized') {
            predictionText.textContent = 'Unrecognized';
            resultIcon.className = 'result-icon fas fa-question-circle status-unknown';
            confidenceFill.style.width = `${data.confidence * 100}%`;
            confidenceText.textContent = `${(data.confidence * 100).toFixed(1)}%`;
            resultMessage.textContent = data.message;
            diseaseInfo.hidden = true;
            return;
        }
        
        // Display prediction results
        predictionText.textContent = data.prediction;
        confidenceFill.style.width = `${data.confidence * 100}%`;
        confidenceText.textContent = `${(data.confidence * 100).toFixed(1)}%`;
        resultMessage.textContent = data.message;
        
        // Set icon and color based on prediction
        if (data.prediction === 'Healthy') {
            resultIcon.className = 'result-icon fas fa-check-circle status-healthy';
        } else {
            resultIcon.className = 'result-icon fas fa-virus status-disease';
        }
        
        // Display disease information
        if (data.disease_info) {
            diseaseInfo.hidden = false;
            
            // Symptoms
            renderList(symptomsList, data.disease_info.symptoms);
            
            // Pesticides
            renderList(pesticidesList, data.disease_info.pesticides);
            
            // Prevention
            renderList(preventionList, data.disease_info.prevention);
        } else {
            diseaseInfo.hidden = true;
        }
    }
    
    function renderList(listElement, items) {
        listElement.innerHTML = '';
        
        if (items && items.length > 0) {
            items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                listElement.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'No information available';
            listElement.appendChild(li);
        }
    }
    
    function showError(message) {
        errorInfo.hidden = false;
        errorMessage.textContent = message;
        diseaseInfo.hidden = true;
        predictionText.textContent = 'Error';
        resultIcon.className = 'result-icon fas fa-exclamation-circle status-disease';
        confidenceFill.style.width = '0%';
        confidenceText.textContent = '0%';
        resultMessage.textContent = '';
    }
    
    function resetResultsDisplay() {
        errorInfo.hidden = true;
        diseaseInfo.hidden = false;
        symptomsList.innerHTML = '';
        pesticidesList.innerHTML = '';
        preventionList.innerHTML = '';
    }
    
    function resetUI() {
        uploadArea.hidden = false;
        previewContainer.hidden = true;
        previewImage.src = '';
        fileInput.value = '';
    }
});