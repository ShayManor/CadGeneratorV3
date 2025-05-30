import os
import json
from pathlib import Path
from flask import Blueprint, render_template, request, jsonify, send_file
from flasgger import Swagger

from flask_cors import CORS
import sys
import traceback
from src.services.create_model import create_full_model

bp = Blueprint('main', __name__)
CORS(bp)


@bp.route('/create_model', methods=['POST'])
def create_model():
    """
        Create a new model
        ---
        tags:
          - Model
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  name:
                    type: string
                  size:
                    type: integer
                required: [name]
        responses:
          201:
            description: model created
          400:
            description: bad request
        """
    data = request.get_json(silent=True) or request.form
    prompt = data.get('prompt')
    name = data.get('name', 'model')
    iters = int(data.get('iterations', 1))

    if not prompt:
        return jsonify(error='Missing prompt'), 400

    try:
        path = create_full_model(prompt, name, iters)
    except Exception as e:
        traceback.print_exception(type(e), e, sys.exc_info()[2])
        return jsonify(error=str(e)), 500

    return send_file(path,
                     as_attachment=True,
                     download_name=f'{name}.stl',
                     mimetype='application/sla')


def create_model_2(data):
    try:
        iterations: int = int(data.get('iterations', 1))
        prompt: str = data['prompt']
        name: str = data['name']
        if not prompt:
            return 400
        create_full_model(prompt, name, iterations)
    except Exception as e:
        traceback.print_exception(type(e), e, sys.exc_info()[2])
        formatted_trace = traceback.format_exception(type(e), e, sys.exc_info()[2])
        print("".join(formatted_trace))
        return 500
    return 200


@bp.route('/get_model', methods=['POST'])
def get_model():
    """
        Get a model from a name
        ---
        tags:
          - Model
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  name:
                    type: string
                required: [name]
        responses:
          200:
            description: model received
          400:
            description: bad request
        """
    try:
        data = request.get_json(silent=True) or request.form
        name = data.get('name')
        if not name:
            return jsonify({"error": "Missing prompt"}), 400
        for file in os.listdir('src/data'):
            if file.endswith('.png'):
                os.remove(os.path.join('src/data', file))
        return send_file(f'src/data/{name}.stl',
                         as_attachment=True,
                         download_name=f'{name}.stl',
                         mimetype='application/sla')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/get_all_models', methods=['GET'])
def get_all_models():
    try:
        pass
    except Exception as e:
        return jsonify({"error": str(e)}), 500
