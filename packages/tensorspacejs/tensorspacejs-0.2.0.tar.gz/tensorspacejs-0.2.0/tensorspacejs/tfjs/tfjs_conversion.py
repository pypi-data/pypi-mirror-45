"""
@author zchholmes / https://github.com/zchholmes
@author syt123450 / https://github.com/syt123450
"""

import os
import subprocess
from utility.file_utility import valid_file, valid_directory, show_invalid_message


MAIN_JS_PATH = os.path.abspath(
    os.path.join(__file__, os.pardir, 'main.js')
)


def process_tfjs_model(path_input, path_output, output_names=None):
    os.makedirs(path_output, exist_ok=True)
    if not valid_file(path_input):
        show_invalid_message('input model file', path_input)
        return

    if output_names is None:
        subprocess.check_call(["node", MAIN_JS_PATH, path_input, path_output])
    else:
        output_names = "--output_layer_names=" + output_names
        subprocess.check_call(["node", MAIN_JS_PATH, output_names, path_input, path_output])

    print("Mission Complete!!!")


def show_tfjs_model_summary(path_input):
    if not valid_file(path_input):
        show_invalid_message('input model file', path_input)
        return

    subprocess.check_call(["node", MAIN_JS_PATH, "--summary", path_input])
