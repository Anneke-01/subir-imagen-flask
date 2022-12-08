#Código de: https://tutorial101.blogspot.com/2021/11/python-flask-upload-multiple-images-and.html
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from pathlib import Path

app = Flask(__name__)

UPLOAD_FOLDER = 'static/files/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    # Tomado de: https://stackoverflow.com/questions/57451177/python3-create-list-of-image-in-a-folder
    # specify the img directory path
    path = "static/files"
    # list files in img directory
    files = os.listdir(path)
    img_path = []
    for file in files:
        if file.endswith(('.jpg', '.png', 'jpeg')):
            img_path.append(file)
    return render_template('index.html',img_path=img_path)

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return redirect("/")
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect("/")

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='files/' + filename), code=301)