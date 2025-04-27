from flask import Flask
from src.routes.routes import bp as main_bp

app = Flask(__name__,
            static_folder='static',
            static_url_path='/static')
app.register_blueprint(main_bp)


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)