from flask import Flask, render_template, request, send_file
import subprocess
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']
        if file.filename == '':
            return "No selected file"

        file.save('uploads/' + 'sipoc_table.csv')  # Save the uploaded file
        logging.info("CSV file saved successfully.")

        # Call your Python script with the uploaded file as an argument
        subprocess.run(['python', 'sipoc-to-pptx-4-Flask.py', 'uploads/' + file.filename])
        logging.info("Python script executed successfully.")

        return "File uploaded and processed successfully"
    except Exception as e:
        # Log any exceptions that occur
        logging.error(f'An error occurred: {str(e)}')
        return "An error occurred while processing the file."


if __name__ == '__main__':
    app.run(debug=True)
