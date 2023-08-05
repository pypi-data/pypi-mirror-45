
'''
Utilities module responsible for global methods for reading files, managing folders.
'''

import os
import glob
from datetime import datetime
import time
from functools import wraps

def prepare_to_train(config_dict):
    save_model_path = config_dict['paths']['save_model_path']
    model_name = config_dict['parameters']['model_name']
    model_path = make_folder_to_model(save_model_path, model_name)
    config_dict['paths']['original_model_path'] = model_path
    return config_dict

def timed(func):
    """This decorator prints the execution time for the decorated function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed_time = end - start
        return result, elapsed_time
    return wrapper

def get_photos_from_dir(images_path):
	extentions = ['*.jpg', '*.png', '*.jpeg']
	filenames = []
	for ext in extentions:
		filenames_temp = glob.glob(os.path.join(images_path, ext))
		filenames += filenames_temp
	if len(filenames) == 0:
		print('No images found in {}!!!'.format(images_path))
	return filenames

def make_folder_to_model(path_to_models_folder, model_name =""):

    if not os.path.exists(path_to_models_folder):
        os.makedirs(path_to_models_folder)

    now = datetime.now()
    date = now.strftime("%Y-%m-%d-%H-%M-%S")
    model_path = os.path.join(path_to_models_folder, '_'.join([model_name, date]))
    os.makedirs(model_path)

    return model_path


def create_folder(folder):          
    if not os.path.exists(folder):
        os.makedirs(folder)

def prepare_folder_in_directory(root_dir, folder_name):
    try:
        output_path = os.path.join(root_dir, folder_name)
        create_folder(output_path)
        return output_path
    except:
        print("Cannot create folder in specified path: {} in {}".format(folder_name, root_dir))

def cleaning_weights_in_folder(model_folder_path, filter_keyword='weights'):
    filenames = os.listdir(model_folder_path)

    weights = [x for x in filenames if filter_keyword in x]
    weights.sort()

    weigths_log = ''
    for weights_to_remove in weights[:-1]:
        file_to_remove = os.path.join(model_folder_path, weights_to_remove)
        weigths_log += os.path.basename(file_to_remove)+'\n'
        os.remove(file_to_remove)
        print("Removing: {}".format(weights_to_remove))

    with open(os.path.join(model_folder_path, "weights_log.txt"), "w") as text_file:
        text_file.write("Weights: \n{}".format(weigths_log))

    file_to_rename = os.path.join(model_folder_path, weights[-1])
    final_weigths_path = os.path.join(model_folder_path, "final_weights.h5")
    os.rename(file_to_rename, final_weigths_path)
    print("Renaming {} to \"final_weights.h5\"".format(os.path.basename(file_to_rename)))

    return final_weigths_path