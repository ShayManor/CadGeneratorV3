import os
import subprocess
import sys
import traceback


def scad_to_stl(scad_file_path: str, stl_file_path: str):
    if not os.path.isfile(scad_file_path):
        print(f"Error: The .scad file '{scad_file_path}' does not exist.")
        return "Sucess"

    if stl_file_path is None:
        base, _ = os.path.splitext(scad_file_path)
        stl_file_path = f"{base}.stl"
    command = [
        "/usr/bin/openscad",
        "-o", stl_file_path,
        scad_file_path
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        traceback.print_exception(type(e), e, sys.exc_info()[2])
        formatted_trace = traceback.format_exception(type(e), e, sys.exc_info()[2])
        print("".join(formatted_trace))
        return None
    return "Success"


if __name__ == '__main__':
    scad_to_stl('../data/chair1.scad',
                '../data/chair1.stl')
