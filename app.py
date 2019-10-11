import os

from flask import Flask, escape, request, render_template, flash, redirect, session, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from db import engine, create_session
from sism.models import Catalog
from sism.tables import create_tables

from helpers.flask import allowed_file

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['SECRET_KEY'] = '4JABe2EkcN3MPC8ONh9q'

Bootstrap(app)


create_tables(engine)


@app.route('/')
def index():
    return redirect(url_for('query'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    import time
    if request.method == 'POST':
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
            f = file.stream.read().decode("utf-8")
            rows = [row.split(",") for row in f.split("\n")]
            db_session = create_session(engine)
            Catalog.from_csv_list(rows).save_to_db(db_session)
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], time.strftime(f"%Y%m%d-%H%M%S.{ext}")))
            flash('Les données ont bien été importées')

    return render_template('upload.html')


@app.route('/query', methods=['GET', 'POST'])
def query():
    import uuid
    from datetime import datetime
    if request.method == 'POST':
        float_params = ['lat_min', 'lat_max', 'long_min', 'long_max',
                        'depth_min', 'depth_max', 'mag_min', 'mag_max']
        date_params = ['date_min', 'date_max']

        def convert_type(key, param):
            if not param:
                return None
            if key in float_params:
                return float(param)
            elif key in date_params:
                return datetime.strptime(param, "%Y-%m-%dT%H:%M:%S.%fZ")

        query_params = {key: convert_type(key, value)
                        for key, value in request.form.items()}
        query_id = uuid.uuid1()
        session[f"query_{query_id}"] = query_params
        return redirect(url_for('results',
                                query_id=query_id))
    return render_template('query.html')


@app.route('/results/<query_id>', methods=['GET'])
def results(query_id):
    query_params = session.get(f"query_{query_id}")
    db_session = create_session(engine)
    catalog = Catalog.from_query(db_session, query_params)
    catalog_big=catalog.keep_biggest()
    attribute_histogramme="mag" #"depth"
    stats, histo_img = catalog.stats_catalog(attribute_histogramme)
    map_html = catalog.map_catalogue()
    return render_template('results.html', earthquakes=catalog, stats=stats, catalog_big=catalog_big, histo_img=histo_img, map_html=map_html)

