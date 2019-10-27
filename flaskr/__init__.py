import os
from flask import Flask

def create_app(test_config=None):
    # create and config the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY = "dev",
        DATABASE = os.path.join(app.instance_path, "flask.sqlite"),
        UPLOAD_FOLDER = os.path.join(app.instance_path, "uploads")
    )

    if test_config is None:
        # load the instance cofig, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exitst
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello from flask!"
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import file
    app.register_blueprint(file.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app