import os
from idlelib.run import flush_stdout

import mss
import numpy as np
import trimesh
from PIL import Image
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from src.helpers.create_path import create_path, get_image_name
from src.helpers.gpt import prompt_image, prompt_text
from src.helpers.scad_to_stl import scad_to_stl

directions = {
    "front": np.array([0, -1, 0]),
    "rightfront": np.array([0.5, -0.5, 0]),
    "leftfront": np.array([-0.5, -0.5, 0]),
    "back": np.array([0, 1, 0]),
    "left": np.array([-1, 0, 0]),
    "right": np.array([1, 0, 0]),
    "top": np.array([0, 0, 1]),
    "bottom": np.array([0, 0, -1])
}
rows, cols = 2, 4

initial_assistant = "asst_oQcmjRALDMEG7V0mlFCYQw2z"


def initial_prompt(
        prompt): return f"Write professional-grade, clean, and well-commented OpenSCAD (.scad) code that fully implements the following object: {prompt} The code should: Be modular and use functions or modules to encapsulate different parts (e.g., legs, base, backrest). Follow good code standard such as always using brackets for if, else, for, etc. Only return code with no explanation before or after. Include comments explaining key components and logic. Be syntactically correct and render without errors or warnings in OpenSCAD. Use correct dimensions and proportions that match the description, with realistic scale.Allow for basic customization via parameters (e.g., chair height, armrest width). Avoid overlapping geometry and ensure everything is solidly unioned."


second_assistant = "asst_dsTGLjdkFmW6ytKRTd87MdNo"


def second_prompt(prompt, code,
                  feedback): return f"You are given the user's original prompt, their feedback on the current design, and the existing OpenSCAD code. Using this context, rewrite the entire OpenSCAD (.scad) file from scratch. Only return code, nothing else. Follow good code standard such as always using brackets for if, else, for, etc. Make the simple changes, for example if you need to remove a piece, just remove it. Your new version should fully reflect the original design intent and address all the feedback. Structure your code cleanly, use modular components where appropriate, and include helpful comments explaining your design. Ensure the code is fully self-contained, compiles without errors or warnings in OpenSCAD, and results in a professional, realistic model. Do not leave any part of the model or feedback unaddressed, and overwrite the entire code file with your improved version. Original prompt: {prompt}, previous code: {code}, updated feedback: {feedback}"


def describe_prompt(
        prompt): return f"You are a professional describer for a cad model who recieves the perspectives and is tasked with giving improvements for how to make it better. This image is supposed to be a {prompt}. Structure your response as score:description where score is a number (worst) 1-5 (best) describing how close the image is to the prompt. Be simple and straight to the point, you are giving instructions to fix it. Be detailed and descriptive. Only go over the things that need changing and be concise, for example if there is an extra piece, just say there is an extra piece, don't cover things that are already good."


bug_fix_assistant = "asst_72OVgDJbiEb0U30WqD7gt5dL"


def fail_prompt(status, prompt,
                prev_code): return f"This code does not compile and returns the error {status}.This is what is being tried to make: {prompt} and this is the old code to rewrite: {prev_code}"


def get_code(prompt: str, prev_code: str, feedback: str, status: str | None) -> str:
    if status:
        code = prompt_text(fail_prompt(status, prompt, prev_code), assistant=bug_fix_assistant)
    else:
        code = prompt_text(initial_prompt(prompt), assistant=initial_assistant) if feedback is None else prompt_text(
            second_prompt(prompt, prev_code, feedback), assistant=second_assistant)
    code = code.replace('```python', '')
    code = code.replace('```scad', '```')
    code = code.replace('```openscad', '')
    code = code.replace('```cad', '')
    code = code.replace('```OpenSCAD', '')
    code = code.replace('```', '')
    return code


def create_model(prompt: str, path: str, feedback: str = None, status: str = None):
    """
    Creates cad model from updated feedback and prompt
    :param status: Error code
    :param path: Path to model
    :param prompt: Original prompt to create model
    :param feedback: Feedback from previous model, can be None
    :return: Nothing
    """
    prev_code = None
    if feedback is not None:
        with open(path, 'r') as f:
            prev_code = "\n".join(f.readlines())
    code = get_code(prompt, prev_code, feedback, status)
    with open(path, 'w') as f:
        f.writelines(code)


def take_screenshots(path: str):
    """
    Headless mesh snapshots using Matplotlib 3D.
    Loads the mesh via trimesh, then captures six orthographic views.
    """
    mesh = trimesh.load_mesh(path)
    verts = mesh.vertices
    faces = mesh.faces

    # center & scale so all views share the same framing
    center = verts.mean(axis=0)
    halfspan = (verts.max(axis=0) - verts.min(axis=0)).max() / 2.0

    # true view angles: (azimuth, elevation)
    angles = {
        "front": (0, 0),
        "rightfront": (-45, 15),
        "leftfront": (45, 15),
        "right": (-90, 0),
        "back": (180, 0),
        "left": (90, 0),
        "top": (0, 90),
        "bottom": (0, -90)
    }

    for view_name, (azim, elev) in angles.items():
        fig = plt.figure(figsize=(4, 4))
        ax = fig.add_subplot(111, projection="3d")

        # add the mesh
        poly = Poly3DCollection(
            verts[faces],
            facecolor=(0.7, 0.7, 0.7),
            edgecolor="k",
            linewidths=0.05,
            alpha=1.0
        )
        ax.add_collection3d(poly)

        # lock in an equal aspect box
        ax.set_xlim(center[0] - halfspan, center[0] + halfspan)
        ax.set_ylim(center[1] - halfspan, center[1] + halfspan)
        ax.set_zlim(center[2] - halfspan, center[2] + halfspan)
        ax.set_box_aspect((1, 1, 1))

        # set the camera
        ax.view_init(elev=elev, azim=azim)

        ax.axis("off")
        plt.tight_layout()

        # write out
        out = get_image_name(view_name)
        fig.savefig(out, dpi=300)
        plt.close(fig)


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
    final_image.save(final_image_path + ".png")

    for view_name in directions.keys():
        path = get_image_name(view_name)
        if not os.path.exists(path):
            continue
        os.remove(path)
    return final_image_path + ".png"


def get_feedback(prompt: str, path: str, name: str) -> str:
    take_screenshots(path)
    final_image_path = combine_screenshots(f"src/data/{name}")
    feedback = prompt_image(describe_prompt(prompt), final_image_path)
    return feedback


def create_full_model(prompt: str, name: str, iterations: int = 1) -> str:
    """
    Creates the cad model for the given params. First gets feedback and uses it to create the new model.
    :param name: Name of cad model
    :param iterations: Number of iterations
    :param prompt: Prompt to create cad model
    :return: Path to created cad model
    """
    path = f"src/data/{name}.scad"
    try:
        open(path, 'x')
    except FileExistsError as e:
        pass
    feedback = None
    iteration = 0
    while iteration < iterations:
        stl_path = path.replace('scad', 'stl')
        print(f"Begin iteration {iteration + 1}")
        create_model(prompt, path, feedback, None)
        status = scad_to_stl(path, stl_path)
        if status:
            print(f"Status is {status}")
            create_model(prompt, path, feedback, status)
            iteration -= 1
            continue
        feedback = get_feedback(prompt, stl_path, name)
        # print(f"Feedback: {feedback}")
        path = create_path(name) + ".scad"
        # create_model(prompt, path, feedback)
    return path
