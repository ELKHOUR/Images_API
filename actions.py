from tkinter import Image

from flask import Blueprint, request, jsonify, redirect, url_for
from PIL import Image
from helpers import chek_file
bp = Blueprint('actions', __name__, url_prefix='/actions')



@bp.route('/resize', methods=['POST'])
def resize():
    file = request.json['filename']
    filename, filepath = chek_file(file)
    if request.method == 'POST':
        try:
            width, height = int(request.json['width']), int(request.json['height'])
            image = Image.open(filepath)
            out = image.resize((width, height))
            out.save(filepath)
            return redirect(url_for('download_file', name=filename))
        except FileNotFoundError:
            return jsonify({'error': 'invalid file'}), 404



@bp.route('/presets/<preset>', methods=['POST'])
def presets(preset):
    presets = {'small': (640, 480), 'medium': (1280, 960), 'large': (1600, 1200)}
    if preset not in presets:
        return jsonify({'error': f'invalid preset, please chose from this :{list(presets.keys())}'}), 400

    file = request.json['filename']
    filename, filepath = chek_file(file)

    try:
        size = presets[preset]
        image = Image.open(filepath)
        out = image.resize(size)
        out.save(filepath)
        return redirect(url_for('download_file', name=filename))
    except FileNotFoundError:
        return jsonify({'error': 'invalid file'}), 404


@bp.route('/rotate', methods=['POST'])
def rotate():
    file = request.json['filename']
    filename, filepath = chek_file(file)
    if request.method == 'POST':
        try:
            degree = int(request.json['degree'])
            image = Image.open(filepath)
            out = image.rotate(degree)
            out.save(filepath)
            return redirect(url_for('download_file', name=filename))
        except FileNotFoundError:
            return jsonify({'error': 'invalid file'}), 404



@bp.route('/flip', methods=['POST'])
def flip():
    file = request.json['filename']
    filename, filepath = chek_file(file)
    try:
        image = Image.open(filepath)
        out = None
        if request.json['direction'] == 'horizontal':
            out = image.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            out = image.transpose(Image.FLIP_LEFT_RIGHT)
        out.save(filepath)
        return redirect(url_for('download_file', name=filename))
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404








