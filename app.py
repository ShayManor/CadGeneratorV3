import os

from flasgger import Swagger
from flask import Flask, jsonify, request, abort
from src.routes.routes import bp as main_bp


def require_api_key(app):
    VALID_KEY = os.getenv("API_KEY")
    @app.before_request
    def check_key():
        if request.path in ("/", "/ping", "/apidocs"):
            return
        if not os.path.exists('src/data'):
            os.mkdir('src/data')
        print(request.headers.get("X-API-Key"))
        if request.headers.get("X-API-Key") != VALID_KEY:
            abort(401, description="Invalid or missing API key")


app = Flask(__name__,
            static_folder='static',
            static_url_path='/static')
app.register_blueprint(main_bp)
swagger = Swagger(app)
require_api_key(app)


@app.route("/ping")
def ping():
    """Health check
    ---
    responses:
      200:
        description: simple uptime probe
    """
    return jsonify({"ping": "pong"})


@app.route('/')
def index():
    """Get webpage
    ---
    responses:
      200:
        description: Gets HTML frontend
    """
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
