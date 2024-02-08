from flask import Flask, render_template, request, send_file
import subprocess
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

try:
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route('/upload', methods=['POST'])
    def upload():
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']
        if file.filename == '':
            return "No selected file"

        file.save('uploads/' + 'sipoc_table.csv')  # Save the uploaded file
        print("Debugging: Reached line 21")
        # Call your Python script with the uploaded file as an argument
        subprocess.run(['python', 'sipoc-to-pptx-4-Flask.py', 'uploads/' + file.filename])
        print("Debugging: Reached line 25")
        return "File uploaded and processed successfully"

except Exception as e:
    # Log the error message
    logging.error(f'An error occurred: {str(e)}')

    

if __name__ == '__main__':
    app.run(debug=True)
