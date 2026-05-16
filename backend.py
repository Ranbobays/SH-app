from flask import Flask, request
import pdfplumber

app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <button type="submit">Upload</button>
    </form>
    '''

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    return f"<pre>{text}</pre>"

app.run(debug=True)