from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename
# import jsonify
import os
import shutil
import easyocr
import pytesseract
import PyPDF2
import pandas as pd
from pymongo import MongoClient
import spacy
# file imported of extracted data
# from comp_name import extract_company_name
# from amount import extract_amount
# from date import dates

nlp = spacy.load("/home/aarika/Desktop/OCR/model-best")

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
        result = reader.readtext(image, detail=0, paragraph=True)
        for line in result:
            print(line)
            text = line
        
    except Exception as e:
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

def process_directory(input_dir,output_dir):
    # data = []
    print(user)
    df1 = pd.DataFrame(columns=["TYPE_OF_BILL","NAME","COMPANY_NAME","INVOICE_NO","DATE","TAX_TYPE","TAX_RATE","DESCRIPTION","AMOUNT","ADDRESS","STATE","COUNTRY","EMAIL","MOBILE","TIME"])
    for root, dirs, filenames in os.walk(input_dir):
    # for filenames in os.walk(input_dir):
        for filename in filenames:
            input_path = os.path.join(input_dir, filename)
            text = process_file(input_path)
            # print(text)
            print("Processed text:")
            doc = nlp(text)
            mylist = []
            for ent in doc.ents:
                print(ent.text, ent.label_)
                mylist.append([ent.text, ent.label_])
            print(mylist)
            type_bill = ','.join(i[0] for i in mylist if i[1] == 'TYPE_OF_BILL')
            name = ','.join(i[0] for i in mylist if i[1] == 'NAME')
            comp_name = ','.join(i[0] for i in mylist if i[1] == 'COMPANY_NAME')
            invoice = ','.join(i[0] for i in mylist if i[1] == 'INVOICE/BILL_NO')
            date = ','.join(i[0] for i in mylist if i[1] == 'DATE')
            tax_type = ','.join(i[0] for i in mylist if i[1] == 'TAX_TYPE')
            tax = ','.join(i[0] for i in mylist if i[1] == 'TAX_RATE')
            description = ','.join(i[0] for i in mylist if i[1] == 'DESCRIPTION')
            amount = ','.join(i[0] for i in mylist if i[1] == 'AMOUNT')
            address = ','.join(i[0] for i in mylist if i[1] == 'ADDRESS')
            country = ','.join(i[0] for i in mylist if i[1] == 'COUNTRY')
            state = ','.join(i[0] for i in mylist if i[1] == 'STATE')
            # quantity = ','.join(i[0] for i in mylist if i[1] == 'QUANTITY')
            email = ','.join(i[0] for i in mylist if i[1] == 'EMAIL')
            mobile = ','.join(i[0] for i in mylist if i[1] == 'MOBILE_No')
            time = ','.join(i[0] for i in mylist if i[1] == 'TIME')
            if user == 'zoho':
                row = pd.DataFrame([[type_bill, name, comp_name, invoice,date, tax_type, tax, description,amount,address,state,country,email,mobile, time]],columns=["TYPE_OF_BILL","NAME","COMPANY_NAME","INVOICE_NO","DATE","TAX_TYPE","TAX_RATE","DESCRIPTION","AMOUNT","ADDRESS","STATE","COUNTRY","EMAIL","MOBILE","TIME"])
                df2 = pd.concat([df1,row])
                print(df2)
            elif user == 'tally':
                row = pd.DataFrame([[type_bill, name, comp_name, invoice,date, tax_type, tax, description,amount,address,state,country,email,mobile, time]],columns=["TYPE_OF_BILL","NAME","COMPANY_NAME","INVOICE_NO","DATE","TAX_TYPE","TAX_RATE","DESCRIPTION","AMOUNT","ADDRESS","STATE","COUNTRY","EMAIL","MOBILE","TIME"])
                df2 = pd.concat([df1,row])
                print(df2)
            elif user == 'q-book':
                row = pd.DataFrame([[type_bill, name, comp_name, invoice,date, tax_type, tax, description,amount,address,state,country,email,mobile, time]],columns=["TYPE_OF_BILL","NAME","COMPANY_NAME","INVOICE_NO","DATE","TAX_TYPE","TAX_RATE","DESCRIPTION","AMOUNT","ADDRESS","STATE","COUNTRY","EMAIL","MOBILE","TIME"])
                df2 = pd.concat([df1,row])
                print(df2)
            else:
                row = pd.DataFrame([[type_bill, name, comp_name, invoice,date, tax_type, tax, description,amount,address,state,country,email,mobile, time]],columns=["TYPE_OF_BILL","NAME","COMPANY_NAME","INVOICE_NO","DATE","TAX_TYPE","TAX_RATE","DESCRIPTION","AMOUNT","ADDRESS","STATE","COUNTRY","EMAIL","MOBILE","TIME"])
                df2 = pd.concat([df1,row])
                print(df2)
            output_path = r"output.html"
            # output_path = os.path.join(output_dir, filename)
            with open(output_path, 'w') as f:
                f.write(f'<html><body><img src="{filename}"><br><pre>{text}</pre></body></html>')
                # f.write(text)
            shutil.move(input_path, output_path)
            print(f"Moved file to {output_path}")
    return df2   

# def extracted_data():
#     amount = extract_amount(amount)
#     date = dates(date)
#     comp_name = extract_company_name(comp_name)
#     df = pd.DataFrame(columns=[])
#     return df
            
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
    df2 = process_directory(input_dir, output_dir)
    insert_data_mongo(df2)
    # return "Data processed and stored in MongoDB!"
    my_data = df2.to_html('/home/aarika/Desktop/OCR/templates/output.html')
    return render_template('output.html', table=my_data)


app.add_url_rule(
    "/<name>/output", endpoint="output.html", build_only=True
)

if __name__ == '__main__':
    # flask.Flask.run()
    app.run(host='0.0.0.0', port=5000, debug=True)