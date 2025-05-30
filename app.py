from flasgger import Swagger
from flask import Flask, jsonify
from src.routes.routes import bp as main_bp

app = Flask(__name__,
            static_folder='static',
            static_url_path='/static')
app.register_blueprint(main_bp)
swagger = Swagger(app)  # docs at /apidocs


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
    app.run(host="0.0.0.0", port=5000, debug=True)
