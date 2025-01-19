from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)

# Set up the folder to store uploaded and cleaned files
UPLOAD_FOLDER = 'uploads'
CLEANED_FOLDER = 'cleaned_data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CLEANED_FOLDER, exist_ok=True)

# Ensure that the app only accepts CSV and Excel files
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_data(file_path):
    # Load the file into pandas DataFrame
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Clean up: remove rows with NaN or empty values
    df.dropna(how='all', inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Check if DataFrame is not empty
    if df.empty:
        return None

    # Save the cleaned data to a new Excel file
    cleaned_filename = 'cleaned_data.xlsx'
    cleaned_filepath = os.path.join(CLEANED_FOLDER, cleaned_filename)

    # Save the cleaned data to an Excel file
    df.to_excel(cleaned_filepath, index=False, sheet_name="Cleaned Data")
    return cleaned_filepath

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Clean the uploaded file
        cleaned_filepath = clean_data(filepath)
        
        if cleaned_filepath:
            return send_file(cleaned_filepath, as_attachment=True)
        else:
            return "No valid data to clean", 400
    else:
        return "Invalid file format. Please upload CSV or Excel files only.", 400

if __name__ == '__main__':
    app.run(debug=True)
