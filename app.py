from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename
# import jsonify
import os
import easyocr
import pytesseract
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
    try:
        text = ""
        reader = easyocr.Reader(['en'])
        result = reader.readtext(file_path, detail=0, paragraph=True)
        for line in result:
            print(line)
            text = line
        
    except Exception as e:
        # print("EasyOCR failed:", e)
        # print("Falling back to PyTesseract OCR...")
        try:
#           grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(image)
            print(text)
        except Exception as e:
            print("PyTesseract OCR failed:", e)

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
                    text += line + " \n "

    return text

def process_directory(input_dir, output_dir):
    df = pd.DataFrame(columns=[])
    for root, dirs, filenames in os.walk(input_dir):
        for filename in filenames:
            input_path = os.path.join(input_dir, filename)
            text = process_file(input_path)
            print(text)
            print("Processed text:")
            doc = nlp(text)
            mylist = []
            for ent in doc.ents:
                print(ent.text, ent.label_)
                mylist.append([ent.text, ent.label_])
            type_bill = ','.join(i[0] for i in mylist if i[1] == 'TYPE_OF_BILL')
            name = ','.join(i[0] for i in mylist if i[1] == 'NAME')
            invoice = ','.join(i[0] for i in mylist if i[1] == 'INVOICE/BILL_NO')
            email = ','.join(i[0] for i in mylist if i[1] == 'EMAIL')
            date = ','.join(i[0] for i in mylist if i[1] == 'DATE')
            description = ','.join(i[0] for i in mylist if i[1] == 'DESCRIPTION')
            amount = ','.join(i[0] for i in mylist if i[1] == 'AMOUNT')
            tax = ','.join(i[0] for i in mylist if i[1] == 'RATE')
            quantity = ','.join(i[0] for i in mylist if i[1] == 'QUANTITY')
            mobile = ','.join(i[0] for i in mylist if i[1] == 'MOBILE_No')
            state = ','.join(i[0] for i in mylist if i[1] == 'STATE')
            address = ','.join(i[0] for i in mylist if i[1] == 'ADDRESS')
            time = ','.join(i[0] for i in mylist if i[1] == 'TIME')
            country = ','.join(i[0] for i in mylist if i[1] == 'COUNTRY')
            tax_type = ','.join(i[0] for i in mylist if i[1] == 'TAX_TYPE')
            
    return df   
            
# data-base CONNECTIONS  
def insert_data_mongo(data):
    client = MongoClient("mongodb+srv://aarika:ajain%40012023@cluster0.y932s1f.mongodb.net/OCR") # connect to MongoDB
    # client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.9.1")
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
# file_handler = FileHandler('errorlog.txt')
# file_handler.setLevel(WARNING)

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
    input_dir = r"/home/aarika/Desktop/OCR/uploads/"
    output_dir = r"/home/aarika/Desktop/OCR/special/"
    df = process_directory(input_dir, output_dir)
    insert_data_mongo(df)
    # return "Data processed and stored in MongoDB!"
    my_data = df.to_html('/home/aarika/Desktop/OCR/templates/output.html')
    return render_template('output.html', table=my_data)


app.add_url_rule(
    "/<name>/output", endpoint="output.html", build_only=True
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)