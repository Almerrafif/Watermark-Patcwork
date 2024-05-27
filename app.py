from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from watermark import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'static/output'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html', watermarked_image=None, extracted_watermark=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    original_file = request.files['original']
    watermark_file = request.files['watermark']

    if original_file and watermark_file:
        original_filename = secure_filename(original_file.filename)
        watermark_filename = secure_filename(watermark_file.filename)
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original.png')
        watermark_path = os.path.join(app.config['UPLOAD_FOLDER'], 'watermark.png')

        original_file.save(original_path)
        watermark_file.save(watermark_path)

        # Apply watermark using Patchwork
        watermarked_image_path = os.path.join(app.config['OUTPUT_FOLDER'], 'watermarked_image.png')
        apply_watermark_patchwork(original_path, watermark_path, watermarked_image_path)

        # Extract watermark using Patchwork
        extracted_watermark_path = os.path.join(app.config['OUTPUT_FOLDER'], 'extracted_watermark.png')
        extract_watermark_patchwork(watermarked_image_path, original_path, extracted_watermark_path)

        return render_template('index.html',
                               watermarked_image='output/watermarked_image.png',
                               extracted_watermark='output/extracted_watermark.png')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
