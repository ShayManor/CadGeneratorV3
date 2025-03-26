import os
import subprocess


def scad_to_stl(scad_file_path: str, stl_file_path: str):
    if not os.path.isfile(scad_file_path):
        print(f"Error: The .scad file '{scad_file_path}' does not exist.")
        return

    if stl_file_path is None:
        base, _ = os.path.splitext(scad_file_path)
        stl_file_path = f"{base}.stl"

    command = [
        'openscad',
        '-o', stl_file_path,
        scad_file_path
    ]
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout:
        print(result.stdout.decode())
    if result.stderr:
        print(result.stderr.decode())
