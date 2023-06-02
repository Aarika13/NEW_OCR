from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import easyocr
import PyPDF2
import pandas as pd
from pymongo import MongoClient


# nlp = spacy.load("/home/aarika/Desktop/OCR/model-best")

def process_file(file_path):
    text = ""
    if file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".png"):
        text = process_image(file_path)
    elif file_path.endswith(".pdf"):
        text = process_pdf(file_path)
    else:
        print("Unsupported file type")
    return text

def process_image(image):
    text = ""
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_path, detail=0, paragraph=True)
    for line in result:
        print(line)
        text = line
    return text

def process_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            lines = page_text.split("\n")

            for line in lines:
                if line.strip():  # Exclude empty lines
                    text += line + "\n"

    return text

    

def process_directory(input_dir, output_dir):
    pass

# data-base CONNECTIONS  
def insert_data_mongo(data):
    # client = MongoClient("mongodb+srv://aarika:ajain%40012023@cluster0.y932s1f.mongodb.net/OCR") # connect to MongoDB
    client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.9.1")
    db = client["OCR"]  # get the database
    collection = db["my_collection"]  # get the collection
    data = data.to_dict(orient="records")
    if data:
        result = collection.insert_many(data)
        print(result.inserted_ids)
    else:
        print("The list of documents is empty.")

UPLOAD_FOLDER = '/home/aarika/Desktop/OCR/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app = Flask(__name__, template_folder="templates")
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def upload():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global user
    user = request.form.get('comp_select')
    print(user)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            # windows.alert("Input the correct file")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
            return redirect(url_for('process_data_route', name=filename))
            # output_data = "/home/sunil/Desktop/np/templates/output.html"
            # return redirect(url_for(output_data,name=filename))
    return render_template("success.html")
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route("/process_data", methods=['GET', 'POST'])
def process_data_route():
    # print(df)
    input_dir = r"/home/sunil/Desktop/np/uploads/"
    output_dir = r"/home/sunil/Desktop/np/special/"
    df = process_directory(input_dir, output_dir)
    insert_data_mongo(df)
    # return "Data processed and stored in MongoDB!"
    my_data = df.to_html('/home/sunil/Desktop/np/templates/output.html')
    return render_template('output.html', table=my_data)


app.add_url_rule(
    "/<name>/output", endpoint="output.html", build_only=True
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)