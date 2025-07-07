// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const singleFeedbackForm = document.getElementById('singleFeedbackForm');
    const batchForm = document.getElementById('batchForm');
    const sampleButtons = document.querySelectorAll('.btn-sample');

    // --- Event Listeners ---
    if (singleFeedbackForm) {
        singleFeedbackForm.addEventListener('submit', handleSingleFeedbackSubmit);
    }

    if (batchForm) {
        batchForm.addEventListener('submit', () => showLoadingSpinner(true));
    }

    sampleButtons.forEach(button => {
        button.addEventListener('click', function() {
            tryExample(this.dataset.example);
        });
    });
});

function showLoadingSpinner(isBatch = false) {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.querySelector('p').textContent = isBatch ? 'Processing file...' : 'Classifying...';
        spinner.style.display = 'flex';
    }
}

function hideLoadingSpinner() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.style.display = 'none';
    }
}

async function handleSingleFeedbackSubmit(event) {
    event.preventDefault();
    const feedbackText = document.getElementById('feedbackText').value;
    const resultContainer = document.getElementById('singleResult');

    if (!feedbackText.trim()) {
        alert('Please enter some feedback.');
        return;
    }

    showLoadingSpinner();
    resultContainer.style.display = 'none';

    try {
        const response = await fetch('/classify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ feedback: feedbackText }),
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const data = await response.json();
        displaySingleResult(data.result);

    } catch (error) {
        console.error('Classification Error:', error);
        resultContainer.innerHTML = `<p style="color: red;">Error: Could not classify feedback.</p>`;
        resultContainer.style.display = 'block';
    } finally {
        hideLoadingSpinner();
    }
}

function displaySingleResult(result) {
    const resultContainer = document.getElementById('singleResult');
    const categoryConfidence = (result.category_confidence * 100).toFixed(0);
    const sentimentConfidence = (result.sentiment_confidence * 100).toFixed(0);
    const categoryClass = result.category.toLowerCase();
    const sentimentClass = result.sentiment.toLowerCase();
    
    const sentimentIcons = {
        'positive': 'fas fa-smile',
        'neutral': 'fas fa-meh',
        'negative': 'fas fa-frown'
    };

    const resultHTML = `
        <div class="result-header">
            <h4><i class="fas fa-check-circle"></i> Classification Result</h4>
        </div>
        <div class="result-body">
            <p><strong>Category:</strong> <span class="category-badge ${categoryClass}">${result.category}</span></p>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${categoryConfidence}%;"></div>
                <span class="confidence-text">${categoryConfidence}% Confidence</span>
            </div>
            <hr>
            <p><strong>Sentiment:</strong> <span class="sentiment-badge ${sentimentClass}">
                <i class="${sentimentIcons[sentimentClass] || 'fas fa-question-circle'}"></i>
                ${result.sentiment}
            </span></p>
            <div class="confidence-bar">
                <div class="confidence-fill sentiment" style="width: ${sentimentConfidence}%;"></div>
                <span class="confidence-text">${sentimentConfidence}% Confidence</span>
            </div>
        </div>
    `;
    resultContainer.innerHTML = resultHTML;
    resultContainer.style.display = 'block';
}

// This function now correctly populates the text area
function tryExample(text) {
    const textarea = document.getElementById('feedbackText');
    textarea.value = text;
    textarea.focus();
    // Scroll the form into view smoothly
    textarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
}