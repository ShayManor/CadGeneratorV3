import os

import numpy as np
import pyvista as pv
from PIL import Image

from src.helpers.create_path import create_path, get_image_name
from src.helpers.gpt import prompt_image, prompt_text

directions = {
    "front": np.array([0, -1, 0]),
    "back": np.array([0, 1, 0]),
    "left": np.array([-1, 0, 0]),
    "right": np.array([1, 0, 0]),
    "top": np.array([0, 0, 1]),
    "bottom": np.array([0, 0, -1])
}
rows, cols = 2, 3

def initial_prompt(prompt): return f"Write professional-grade, clean, and well-commented OpenSCAD (.scad) code that fully implements the following object: {prompt} The code should: Be modular and use functions or modules to encapsulate different parts (e.g., legs, base, backrest). Only return code with no explanation before or after. Include comments explaining key components and logic. Be syntactically correct and render without errors or warnings in OpenSCAD. Use correct dimensions and proportions that match the description, with realistic scale.Allow for basic customization via parameters (e.g., chair height, armrest width). Avoid overlapping geometry and ensure everything is solidly unioned."
def second_prompt(prompt, code, feedback): return f"You are given the user's original prompt, their feedback on the current design, and the existing OpenSCAD code. Using this context, rewrite the entire OpenSCAD (.scad) file from scratch. Only return code, nothing else. Your new version should fully reflect the original design intent and address all the feedback. Structure your code cleanly, use modular components where appropriate, and include helpful comments explaining your design. Ensure the code is fully self-contained, compiles without errors or warnings in OpenSCAD, and results in a professional, realistic model. Do not leave any part of the model or feedback unaddressed, and overwrite the entire code file with your improved version. Original prompt: {prompt}, previous code: {code}, updated feedback: {feedback}"


def get_code(prompt: str, prev_code: str, feedback: str) -> str:
    code = prompt_text(initial_prompt(prompt)) if feedback is None else prompt_text(second_prompt(prompt, prev_code, feedback))
    code.replace('```python', '')
    code.replace('```scad', '```')
    code.replace('```openscad', '')
    code.replace('```cad', '')
    code.replace('```OpenSCAD', '')
    code.replace('```', '')
    return code


def create_model(prompt: str, path: str, feedback: str = None):
    """
    Creates cad model from updated feedback and prompt
    :param path: Path to model
    :param prompt: Original prompt to create model
    :param feedback: Feedback from previous model, can be None
    :return: Nothing
    """
    prev_code = None
    if feedback is not None:
        with open(path, 'r') as f:
            prev_code = "\n".join(f.readlines())
    code = get_code(prompt, prev_code, feedback)
    with open(path, 'w') as f:
        f.writelines(code)


def take_screenshots(path: str):
    """
    Takes screenshots of all angles of cad model
    :param path: path to model
    :return: image path
    """

    mesh = pv.read(path)
    xmin, xmax, ymin, ymax, zmin, zmax = mesh.bounds

    center = np.array([(xmax + xmin) / 2.0,
                       (ymax + ymin) / 2.0,
                       (zmax + zmin) / 2.0])
    max_dim = max(xmax - xmin, ymax - ymin, zmax - zmin)

    camera_distance = 1.5 * max_dim

    plotter = pv.Plotter(off_screen=True)  # headless
    plotter.add_mesh(mesh)

    for view_name, direction in directions.items():
        camera_pos = center + direction * camera_distance

        # For top and bottom views, adjust the up vector so we don't get a strange rotation:
        if view_name in ["top", "bottom"]:
            up = [0, 1, 0]
        else:
            up = [0, 0, 1]  # default up

        plotter.set_position(camera_pos)
        plotter.set_focus(center)
        plotter.set_viewup(up)

        plotter.reset_camera_clipping_range()

        plotter.show(auto_close=False)  # Render without closing
        plotter.screenshot(get_image_name(view_name))

    plotter.close()


def combine_screenshots(final_image_path: str) -> str:
    images = []
    border_size = 10
    border_color = (0, 0, 0, 0)

    for view_name in directions.keys():
        path = get_image_name(view_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f'Could not find file {path}')
        images.append(Image.open(path))

    # Ensure images are the same size
    widths, heights = zip(*(i.size for i in images))
    if len(set(widths)) != 1 or len(set(heights)) != 1:
        raise ValueError("All images must have the same dimensions.")

    img_width, img_height = images[0].size

    final_width = (cols * img_width) + ((cols + 1) * border_size)
    final_height = (rows * img_height) + ((rows + 1) * border_size)

    final_image = Image.new('RGBA', (final_width, final_height), border_color)

    for index, img in enumerate(images):
        row_i = index // cols
        col_i = index % cols

        x_offset = border_size + col_i * (img_width + border_size)
        y_offset = border_size + row_i * (img_height + border_size)
        final_image.paste(img, (x_offset, y_offset))

    final_image.save(final_image_path)

    for view_name in directions.keys():
        path = get_image_name(view_name)
        if not os.path.exists(path):
            continue
        os.remove(path)
    return final_image_path


def get_feedback(prompt: str, path: str, name: str) -> str:
    take_screenshots(path)
    final_image_path = combine_screenshots(name)
    feedback = prompt_image(prompt, final_image_path)
    return feedback


def create_full_model(prompt: str, name: str, iterations: int = 1) -> str:
    """
    Creates the cad model for the given params. First gets feedback and uses it to create the new model.
    :param name: Name of cad model
    :param iterations: Number of iterations
    :param prompt: Prompt to create cad model
    :return: Path to created cad model
    """
    path = None
    feedback = None
    for iteration in range(iterations):
        print(f"Begin iteration {iteration + 1}")
        if iteration != 0:
            feedback = get_feedback(prompt, path, name)
            print(f"Feedback: {feedback}")
        path = create_path(name)
        create_model(prompt, path, feedback)
    return path
