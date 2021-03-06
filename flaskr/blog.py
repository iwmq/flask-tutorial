from flask import (Blueprint, flash, g, redirect, render_template, session, request, Response, url_for, send_file, current_app)

from werkzeug.exceptions import abort

from PIL import Image

import io

import os

import glob

from flaskr.auth import login_requred

from flaskr.db import get_db

bp = Blueprint("blog", __name__)

@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)

@bp.route("/create", methods=("GET", "POST"))
@login_requred
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if title is None:
            error = "Title is required."
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)", (title, body, g.user['id']))
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")

def get_post(id, check_author=True):
    db = get_db()
    post = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE p.id = ?",
        (id ,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {} does not exist".format(id))
    
    if check_author and post['author_id'] != g.user["id"]:
        abort(403)

    return post

@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_requred
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if title is None:
            error = "Title is required."
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id))
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)

    return "update " + str(id)

@bp.route("/<int:id>/delete", methods=("POST", ))
@login_requred
def delete(id):
    post = get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))