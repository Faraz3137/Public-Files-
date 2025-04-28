# app.py
from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    result = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            file_type = os.path.splitext(filename)[1]
            size_kb = round(os.path.getsize(filepath) / 1024, 2)
            try:
                with open(filepath, 'rb') as f:
                    f.read()
                health = 'Healthy'
            except Exception:
                health = 'Corrupted'
            result = {
                'filename': filename,
                'file_type': file_type,
                'size_kb': size_kb,
                'health': health
            }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)


# templates/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Upload Inspector</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f4f7fa;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: #fff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 90%;
            max-width: 400px;
        }
        h2 {
            margin-bottom: 1rem;
            color: #333;
        }
        input[type="file"] {
            margin-bottom: 1rem;
        }
        .details {
            margin-top: 1.5rem;
            text-align: left;
            font-size: 0.95rem;
            color: #333;
        }
        .details span {
            font-weight: bold;
        }
        button {
            padding: 0.6rem 1.2rem;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1rem;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Upload a File</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" required><br>
            <button type="submit">Upload</button>
        </form>
        {% if result %}
        <div class="details">
            <p><span>Filename:</span> {{ result.filename }}</p>
            <p><span>File Type:</span> {{ result.file_type }}</p>
            <p><span>Size:</span> {{ result.size_kb }} KB</p>
            <p><span>Health:</span> {{ result.health }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
