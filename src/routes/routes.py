from flask import Blueprint, render_template, request, jsonify

from src.services.create_model import create_full_model

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    pass


@bp.route('/create_model', methods=['POST'])
def create_model():
    print("Here")
    try:
        iterations: int = int(request.args.get('iterations')) | 1
        prompt: str = request.args.get('prompt')
        name: str = request.args.get('name')
        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400
        create_full_model(prompt, name, iterations)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500



@bp.route('/get_model', methods=['POST'])
def get_model():
    try:
        id_num = int(request.args.get('id'))
        if not id_num:
            return jsonify({"error": "Missing prompt"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/get_all_models', methods=['GET'])
def get_all_models():
    try:
        pass
    except Exception as e:
        return jsonify({"error": str(e)}), 500
