from flask import Flask, render_template, request, flash
import os
import PyPDF2
import shutil
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def process_all_pdfs():
    results = []
    pdf_files = Path(UPLOAD_FOLDER).glob('*.pdf')
    
    for pdf_path in pdf_files:
        text = extract_text_from_pdf(pdf_path)
        results.append({
            'filename': pdf_path.name,
            'text': text
        })
    
    # Clean up uploads folder
    shutil.rmtree(UPLOAD_FOLDER)
    os.makedirs(UPLOAD_FOLDER)
    
    return results

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template('upload.html')
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template('upload.html')
        
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process PDFs and get results
            results = process_all_pdfs()
            return render_template('upload.html', results=results)
        else:
            flash('Allowed file type is PDF')
            
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)