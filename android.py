import shutil
from datetime import datetime

from flask import Blueprint, current_app, request, redirect, url_for
import os
from helpers import chek_file
from PIL import Image
from zipfile import ZipFile
from os.path import basename



bp = Blueprint('android', __name__, url_prefix='/android')
ICON_SIZES = [29, 40, 57, 58, 60, 80, 87, 114, 120, 180, 1024]


@bp.route('/', methods=['POST'])
def create_images():
    file = request.json['filename']
    filename, filepath = chek_file(file)

    tempfolder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp')
    os.makedirs(tempfolder)

    for size in ICON_SIZES:
        outfile = os.path.join(tempfolder,f"{size}.png")
        image = Image.open(filepath)
        out = image.resize((size, size))
        out.save(outfile, "PNG")

    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).rsplit('.')[0]
    zipfilename = f"{timestamp}.zip"
    zipfilepath = os.path.join(current_app.config['UPLOAD_FOLDER'], zipfilename)

    with ZipFile(zipfilepath, 'w') as zipObj:
        for foldername, subfolders, filenames in os.walk(tempfolder):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                zipObj.write(filepath, basename(filepath))
        shutil.rmtree(tempfolder)
        return redirect(url_for('download_file', name = zipfilename))