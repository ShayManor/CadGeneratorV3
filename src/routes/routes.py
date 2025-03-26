from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    pass


@bp.route('/create_cad', methods=['POST'])
def create_cad():
    try:
        iterations: int = int(request.args.get('iterations')) | 1
        prompt: str = request.args.get('prompt')
        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/get_cad', methods=['POST'])
def get_cad():
    try:
        id_num = int(request.args.get('id'))
        if not id_num:
            return jsonify({"error": "Missing prompt"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
