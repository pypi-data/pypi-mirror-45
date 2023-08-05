import glob
import os
import re

import numpy as np
import pandas as pd

from segmentation_module.segmentation_tools.utils2 import get_photos_from_dir


def get_images_paths(images_path, dataset):
    filenames = get_photos_from_dir(os.path.join(images_path, dataset))
    return filenames

images_path = r"D:\segmentation_labels_15_04_2019\images"
labels_path = r"D:\segmentation_labels_15_04_2019\labels"
images_path = os.path.normpath(images_path)
labels_path = os.path.normpath(labels_path)

datasets = ['train', 'val', 'test']

for dataset in datasets:

    filenames_im = get_images_paths(images_path, dataset)
    filenames_im = [os.path.join(dataset, os.path.basename(x)) for x in filenames_im]
    filenames_lb =  get_images_paths(labels_path, dataset)
    filenames_lb = [os.path.join(dataset, os.path.basename(x)) for x in filenames_lb]
    concat = np.vstack([filenames_im, filenames_lb]).transpose()
    df = pd.DataFrame(concat, columns=['images', 'labels'])
    df.to_csv(dataset+'.csv', index=False)

# def foobar(images_path, datasets = ['train', 'val', 'test']):

#     images_path = os.path.normpath(images_path)

#     for dataset in datasets:
#         filenames_im = get_images_paths(images_path, dataset)
#         filenames_im = [os.path.join(dataset, os.path.basename(x)) for x in filenames_im]
#         concat = np.vstack([filenames_im, filenames_lb]).transpose()
#         df = pd.DataFrame(concat, columns=['images', 'labels'])
#         df.to_csv(dataset+'.csv', index=False)
