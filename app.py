# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file, session
from werkzeug.utils import secure_filename
import os
import pandas as pd
from io import BytesIO

# --- AI Classifier ---
from classifier import FeedbackClassifier
classifier = FeedbackClassifier()

# --- App Initialization ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key-that-you-should-change'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def handle_classify():
    """Handles single feedback classification requests from the frontend."""
    if not request.json or 'feedback' not in request.json:
        return jsonify({'error': 'Invalid request format'}), 400

    feedback = request.json['feedback']
    try:
        result = classifier.classify(feedback)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def handle_upload():
    """Handles file uploads, classifies the content, and shows the results page."""
    if 'file' not in request.files:
        flash('No file part selected.')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected.')
        return redirect(url_for('index'))

    if file:
        filename = secure_filename(file.filename)
        
        try:
            feedbacks = []
            if filename.endswith('.csv'):
                df = pd.read_csv(file.stream, header=None)
                feedbacks = df.iloc[:, 0].dropna().tolist()
            elif filename.endswith('.txt'):
                feedbacks = [line.decode('utf-8').strip() for line in file.readlines() if line.strip()]
            else:
                flash('Invalid file type. Please use .csv or .txt')
                return redirect(url_for('index'))

            results = classifier.classify_batch(feedbacks)
            
            # Combine original text with results for rendering
            processed_results = [
                {'index': i, 'original_text': feedbacks[i], **results[i]}
                for i, result in enumerate(results)
            ]
            
            # Store results in session to be used for export
            session['last_results'] = processed_results

            return render_template(
                'results.html',
                filename=filename,
                results=processed_results
            )
        except Exception as e:
            flash(f'Error processing file: {str(e)}')

    return redirect(url_for('index'))

@app.route('/export')
def export_results():
    """Exports the last batch results to an Excel file."""
    results = session.get('last_results', [])
    if not results:
        flash('No results to export.')
        return redirect(url_for('index'))

    # Create a Pandas DataFrame
    df = pd.DataFrame([{
        'Feedback': r['original_text'],
        'Category': r['category'],
        'Category Confidence': r.get('category_confidence'),
        'Sentiment': r['sentiment'],
        'Sentiment Confidence': r.get('sentiment_confidence')
    } for r in results])
    
    # Create an in-memory Excel file
    output = BytesIO()
    df.to_excel(output, index=False, sheet_name='Feedback Results')
    output.seek(0)
    
    session.pop('last_results', None) # Clear session data

    return send_file(
        output,
        as_attachment=True,
        download_name='feedback_results.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


if __name__ == '__main__':
    app.run(debug=True, port=5001)