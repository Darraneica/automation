from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML template

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Read the uploaded file into a pandas DataFrame
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        return "Unsupported file format", 400

    # Clean the data (remove empty rows and duplicates)
    df_cleaned = df.dropna().drop_duplicates()

    # Save the cleaned DataFrame to a BytesIO object (Excel file)
    cleaned_excel = BytesIO()
    df_cleaned.to_excel(cleaned_excel, index=False)
    cleaned_excel.seek(0)  # Rewind to the beginning of the file

    return send_file(cleaned_excel, as_attachment=True, download_name="cleaned_data.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == '__main__':
    app.run(debug=True)
