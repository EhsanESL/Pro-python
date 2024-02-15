from flask import Flask, render_template, request, send_file,jsonify
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
            return jsonify({'error': 'No file selected'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        file.save('uploads/' + 'sipoc_table.csv')  # Save the uploaded file
        logging.info("CSV file saved successfully.")

        # Call your Python script with the uploaded file as an argument
        subprocess.run(['python3', 'sipoc-to-pptx-4-Flask.py', 'uploads/' + file.filename])
        logging.info("Python script executed successfully.")

        return jsonify({'message': 'Upload successful'}), 200
    except Exception as e:
        # Log any exceptions that occur
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': 'An error occurred while processing the file'}), 500



@app.route('/download_pptx')
def download_pptx():
    try:
        # Specify the path to the PowerPoint file
        pptx_filename = 'uploads/output_presentation.pptx'
        logging.info("PowerPoint file downloaded successfully.")

        # Return the file as an attachment
        return send_file(pptx_filename, as_attachment=True)
        
        

    except Exception as e:
        # Log any exceptions that occur
        logging.error(f'An error occurred: {str(e)}')
        # Return an error message or redirect to an error page
        return "An error occurred while downloading the file."




if __name__ == '__main__':
    app.run(debug=True)
