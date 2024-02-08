from flask import Flask, render_template, request, send_file
import subprocess
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Define upload status constants
UPLOAD_SUCCESS = "File uploaded and processed successfully"
NO_FILE_SELECTED = "No file selected"

@app.route("/")
def index():
    return render_template('index.html', upload_status="")

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return render_template('index.html', upload_status=NO_FILE_SELECTED)

        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', upload_status=NO_FILE_SELECTED)

        file.save('uploads/' + 'sipoc_table.csv')  # Save the uploaded file
        logging.info("CSV file saved successfully.")

        # Call your Python script with the uploaded file as an argument
        subprocess.run(['python3', 'sipoc-to-pptx-4-Flask.py', 'uploads/' + file.filename])
        logging.info("Python script executed successfully.")

        return render_template('index.html', upload_status=UPLOAD_SUCCESS)
    except Exception as e:
        # Log any exceptions that occur
        logging.error(f'An error occurred: {str(e)}')
        return render_template('index.html', upload_status="An error occurred while processing the file..")


if __name__ == '__main__':
    app.run(debug=True)
