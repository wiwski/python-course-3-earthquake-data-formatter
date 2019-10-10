import os

from flask import Flask, escape, request, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from helpers.flask import allowed_file

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['SECRET_KEY'] = '4JABe2EkcN3MPC8ONh9q'

Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    import time
    if request.method == 'POST':
        print("here")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            ext = filename.split('.')[-1]
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], time.strftime(f"%Y%m%d-%H%M%S.{ext}")))

    return render_template('upload.html')
