from flask import Flask, request, jsonify, send_from_directory
from helpers import allowed_extentions, chek_file
from actions import bp as actionsbp
from filters import bp as filtersbp
from android import bp as androidbp

app = Flask(__name__)

app.register_blueprint(actionsbp)
app.register_blueprint(filtersbp)
app.register_blueprint(androidbp)
app.secret_key = 'SECRET_KEY'


app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = ['jpg', 'jpeg', 'png']


@app.route('/image', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'Not File Selected'}), 400

        file = request.files['file']
        if "" == file.filename:
            return jsonify({'error': 'No File Selected'}), 400

        if not allowed_extentions(file.filename):
            return jsonify({'error': 'Invalid Extension'}), 400

        filename, filepath = chek_file(file.filename)

        file.save(filepath)
        return jsonify({'Image_name': filename, 'message': 'Image saved'}), 201





@app.route('/upload/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)











# from flask import Flask, render_template, request, jsonify, send_from_directory
# from actions import bp as actionsbp
# from filters import bp as filtersbp
# from android import bp as androidbp
# from helpers import allowed_extension, get_secure_filename_filepath
#
#
#
#
# ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
#
# app = Flask(__name__)
#
# app.secret_key = 'SECRET_KEY'
#
# app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
# app.config['UPLOAD_FOLDER'] = './uploads'
#
#
# app.register_blueprint(actionsbp)





# app.register_blueprint(filtersbp)
# app.register_blueprint(androidbp)
#
#
#
# @app.route('/images', methods=['POST'])
# def upload_image():
#     if request.method == 'POST':
#         if "file" not in request.files:
#             return jsonify({'error': 'No any file was selected'}), 400
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No file was selected'}), 400
#         if not allowed_extension(file.filename):
#             return jsonify({'error': f'The extension is not supported: {file.filename} because it is not an image'}), 400
#
#         filename, filepath = get_secure_filename_filepath(file.filename)
#
#         file.save(filepath)
#         return jsonify({
#             'message': "File successfully uploaded",
#             'filename': filename,
#
#         }), 201
#
#
# @app.route('/uploads/<name>')
# def download_file(name):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], name)
#
#
#
#
#
#
#
#
#
