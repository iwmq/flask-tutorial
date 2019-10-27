from flask import (Blueprint, flash, g, redirect, render_template, session, request, Response, url_for, send_file, current_app, send_from_directory)

from werkzeug.utils import secure_filename

from PIL import Image

import os

import io

bp = Blueprint("file", __name__, url_prefix="/file")

def get_thumbnail(filename=None, thumb_width=240):
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(path):
       path = os.path.join(current_app.config["UPLOAD_FOLDER"], "default.jpg")

    im = Image.open(path)
    original_width = im.size[0]
    original_height = im.size[1]

    thumb_height = int((thumb_width / original_width) * original_height) if original_height > thumb_width else original_height
    thumbnail = im.resize((thumb_width, thumb_height))

    thumbnail_buffer = io.BytesIO()
    thumbnail.save(thumbnail_buffer, "jpeg", quality=50)
    thumbnail_buffer.seek(0)

    return thumbnail_buffer

@bp.route("/show_thumbnail/<name>")
def show_thumbnail(name="dog.jpg"):
    thumbnail_buffer = get_thumbnail(name)
    return send_file(thumbnail_buffer, mimetype='image/jpeg')

@bp.route("/image")
def thumbnails():
    img_path = current_app.config["UPLOAD_FOLDER"]
    imgs = filter(lambda x:x.split(".")[-1] in ("jpg", "png", "jpeg"), os.listdir(img_path))
    return render_template("file/image.html", imgs=imgs)

@bp.route("/file_browser")
def file_browser():
    func_num = request.args.get("CKEditorFuncNum")
    return render_template("file/file_browser.html", func_num=func_num)

def allowed_file(filename):
    allowed_extensions = ["png", "jpg", "jpeg", "gif"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

@bp.route("/file_uploader", methods=("GET", "POST"))
def file_uploader():
    message = ""
    js_script = ""

    if request.method == "POST":
        if "upload" not in request.files:
            message = "No file found"

        print(request.files)

        file = request.files["upload"]
        
        if file.filename == "":
            message = "No file found"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            message = "Upload successfully"
        
        func_num = request.args.get("CKEditorFuncNum")
        file_url = url_for("file.uploaded_file", filename=filename)

        js_script = """
            <script>
                window.parent.CKEDITOR.tools.callFunction({}, '{}', '{}')
            </script>
        """.format(func_num, file_url, message)

    return js_script

@bp.route("/<filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)