import os
from flask import Flask, request, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename
from upMongo import upload_to_mongo

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['csv'])

#inciando a aplicação web
app = Flask(__name__, template_folder='template')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'qwerty123!@#'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Processo de envio de arquivo
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Selecione um arquivo para enviar!')
            return render_template('index.html')
        file = request.files['file']
        if allowed_file(file.filename) == False:
            flash('Selecione um arquivo do tipo CSV para enviar!')
            return render_template('index.html')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Arquivo enviado com sucesso!')
            return upload_to_mongo(filename)
        return render_template('index.html')
    return render_template('index.html')

app.run(debug=True)