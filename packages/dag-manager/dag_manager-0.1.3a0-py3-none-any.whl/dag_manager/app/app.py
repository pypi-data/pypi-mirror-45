# -*- coding: utf-8 -*-
# @Time    : 2019-04-09 11:02
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: app.py
# @Software: PyCharm
from flask import Flask, request, flash, redirect

from dag_manager.app.blueprints.dag_ids import dag_ids_blueprint
from dag_manager.app.blueprints.dags import dags_blueprint

app = Flask(__name__)
app.register_blueprint(dags_blueprint)
app.register_blueprint(dag_ids_blueprint)


doc = "<pre>{}</pre>".format('\n'.join([
    str(rule).replace('<', '&lt;').replace('>', '&gt;') + '\t' + str(rule.methods)
    for rule in app.url_map.iter_rules()
]))


@app.route('/')
def index():
    return doc


@app.route('/echo')
def echo():
    return 'ok'


def upload_file():
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
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run()
