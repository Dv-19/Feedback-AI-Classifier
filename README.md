# Feedback AI Classifier 🤖

A web application built with Flask and Transformers that uses AI to classify college feedback by category and sentiment. It includes features for single feedback analysis, batch processing via file upload, a results dashboard with graphs, and an option to export data to Excel.

## ✨ Features

- **AI-Powered Analysis:** Classifies feedback into **Academics, Facilities, and Administration**.
- **Sentiment Analysis:** Determines if feedback is **Positive, Negative, or Neutral**.
- **Interactive UI:** A clean, modern interface for classifying single feedback or uploading batch files (.csv, .txt).
- **Results Dashboard:** Displays a summary of batch results with an interactive chart.
- **Data Export:** Export classified feedback data to an Excel spreadsheet.

## 🛠️ Tech Stack

- **Backend:** Flask, Python
- **AI:** Hugging Face Transformers (`facebook/bart-large-mnli`, `cardiffnlp/twitter-roberta-base-sentiment-latest`)
- **Frontend:** HTML, CSS, JavaScript
- **Charting:** Chart.js

## 🚀 How to Run Locally

1.  **Clone the repository (or set up your files):**
    ```bash
    git clone [your-repo-link]
    cd College_Feedback_Dashboard
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```

5.  Open your browser and navigate to `http://127.0.0.1:5001`.

