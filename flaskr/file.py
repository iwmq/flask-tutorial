from flask import (Blueprint, flash, g, redirect, render_template, session, request, Response, url_for, send_file, current_app)

from PIL import Image

import os

import io

bp = Blueprint("file", __name__, url_prefix="/file")

def get_thumbnail(filename=None, thumb_width=240):
    path = os.path.join(r"d:\repo\flask-tutorial\flaskr\static\img", filename)

    if not os.path.exists(path):
       path = os.path.join(r"d:\repo\flask-tutorial\flaskr\static\img", "default.jpg")

    im = Image.open(path)
    original_width = im.size[0]
    original_height = im.size[1]

    thumb_height = int((thumb_width / original_width) * original_height) if original_height > thumb_width else original_height
    thumbnail = im.resize((thumb_width, thumb_height))

    thumbnail_buffer = io.BytesIO()
    thumbnail.save(thumbnail_buffer, "jpeg", quality=50)
    thumbnail_buffer.seek(0)

    return thumbnail_buffer

@bp.route("/hello")
def hello():
    return "Heloo"

@bp.route("/show_thumbnail/<name>")
def show_thumbnail(name="dog.jpg"):
    thumbnail_buffer = get_thumbnail(name)
    return send_file(thumbnail_buffer, mimetype='image/jpeg')

@bp.route("/image")
def thumbnails():
    img_path = r"d:\repo\flask-tutorial\flaskr\static\img"
    imgs = filter(lambda x:x.split(".")[-1] in ("jpg", "png", "jpeg"), os.listdir(img_path))
    return render_template("file/image.html", imgs=imgs)

@bp.route("/file_browser")
def file_browser():
    func_num = request.args.get("CKEditorFuncNum")
    return render_template("file/file_browser.html", func_num=func_num)