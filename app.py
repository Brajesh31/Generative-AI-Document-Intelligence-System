from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

# AI Engine imports
from ai_engine.ocr_engine import extract_text_from_image
from ai_engine.ner_extractor import extract_named_entities
from ai_engine.summarizer import generate_summary

# PDF processing (digital + OCR hybrid)
from pdf_processor.pdf_text_handler import extract_all_text_from_pdf
from pdf_processor.image_preprocessor import enhance_image

# Config
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Utility: Check allowed file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'document' not in request.files:
            return "No file part"

        file = request.files['document']
        if file.filename == '':
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            # Step 1: Extract text (smart logic based on file type)
            if filename.endswith('.pdf'):
                extracted_text = extract_all_text_from_pdf(save_path)
            else:
                enhanced = enhance_image(save_path)
                extracted_text = extract_text_from_image(enhanced)

            # Step 2: Extract entities and generate summary
            entities = extract_named_entities(extracted_text)
            summary = generate_summary(extracted_text)

            # Step 3: Save outputs
            os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
            base_name = os.path.splitext(filename)[0]
            output_text_path = os.path.join(app.config['OUTPUT_FOLDER'], base_name + '_extracted.txt')
            output_summary_path = os.path.join(app.config['OUTPUT_FOLDER'], base_name + '_summary.txt')

            with open(output_text_path, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            with open(output_summary_path, 'w', encoding='utf-8') as f:
                f.write(summary)

            # Step 4: Show result
            return render_template('result.html',
                                   extracted_text=extracted_text,
                                   summary=summary,
                                   entities=entities,
                                   text_file=base_name + '_extracted.txt',
                                   summary_file=base_name + '_summary.txt')

    return render_template('upload.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Project Info Page
@app.route('/project-info')
def project_info():
    return render_template('project_info.html')

@app.route('/outputs/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=False, host='0.0.0.0', port=port)

