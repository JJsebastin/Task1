"""
app.py  –  PlayStats Flask Web App
Run:  python app.py
"""
from flask import Flask
from web.routes import main_bp


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = "playstats-fifa2026-secret"
    app.register_blueprint(main_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
