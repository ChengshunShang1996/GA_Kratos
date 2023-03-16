from distutils.dir_util import copy_tree
import os
import matplotlib.pyplot as plt

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + "_" + str(counter) + extension
        counter += 1

    return path

aim_file_name = 'current_folder_name'
aim_path = os.path.join(os.getcwd(),'kratos_results_data_temp', aim_file_name)

if not os.path.exists(aim_path):
    os.mkdir(aim_path)

print(aim_path)

aim_path = uniquify(aim_path)

os.mkdir(aim_path)

print(aim_path)

aim_path = uniquify(aim_path)

os.mkdir(aim_path)

print(aim_path)