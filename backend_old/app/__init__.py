
from flask import Flask, jsonify
from flask_cors import CORS

from app.routes.news_routes import bp as news_bp
from app.routes.sentiment_routes import bp as sentiment_bp
from app.routes.bot_routes import bot_bp


def create_app():
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(news_bp, url_prefix="/news")
    app.register_blueprint(sentiment_bp, url_prefix="/sentiment")
    app.register_blueprint(bot_bp, url_prefix="/bot")

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Dristikon AI Backend",
            "status": "running"
        })

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "healthy"}), 200

    return app
