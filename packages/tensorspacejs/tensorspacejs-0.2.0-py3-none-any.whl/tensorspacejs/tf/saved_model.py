"""
@author syt123450 / https://github.com/syt123450
"""

import os
import shutil
from tf.pb2json.pb2json_conversion import convert
import subprocess

input_format_config = '--input_format=tf_saved_model'


def preprocess_saved_model(input_path, output_path, output_node_names):
    print("Preprocessing tensorflow saved model...")
    os.makedirs(output_path + '/tmp', exist_ok=True)
    print("Converting saved model to web friendly format...")
    subprocess.check_call([
        "tensorflowjs_converter",
        input_format_config,
        "--output_node_names=" + output_node_names,
        "--saved_model_tags=serve",
        input_path,
        output_path + '/tmp'
    ])
    path_now = os.getcwd()
    os.chdir(output_path)
    absolute_output_path = os.getcwd()
    absolute_output_path_temp = absolute_output_path + '/tmp/'
    os.chdir(path_now)
    print("Converting pb to json...")
    convert(
        absolute_output_path_temp,
        absolute_output_path
    )
    print("Removing temp pb model...")
    shutil.rmtree(absolute_output_path_temp)
