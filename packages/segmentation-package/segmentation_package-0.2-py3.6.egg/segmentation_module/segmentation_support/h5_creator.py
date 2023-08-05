import glob
import json
import os

import h5py
import numpy as np
import pandas as pd
import PIL.Image as Image
from tqdm import trange

import cv2
from segmentation_module.segmentation_api.api_object import APIObject
from segmentation_module.segmentation_tools.utils2 import get_photos_from_dir


'''[Class responsible for generating h5 file from separated image dataset]
Paths to image folders are specyfied in config file
Images in folders shoudl be placed in specyfic manner (any folder name is allowed)
--data
    --images
        --train
        --val
        --test
    --labels
        --train
        --val
        --test

Creates h5 file in specyfied path
:rtype: [type]
'''

class H5_Creator(APIObject):

    __slots__ = ('csv_path', # comment
                'images_folder',
                'labels_folder',
                'output_width',
                'output_height',
                'is_val_dataset',
                'is_test_dataset')


    def __init__(self, images_folder, labels_folder, csv_train_path, csv_val_path=None, csv_test_path=None):
        """Load csv file with images and corresponding labels
        
        :param csv_path: [Path to csv file]
        :type csv_path: [string]
        :param images_folder: [Path to folder with images and labels]
        :type images_folder: [string]
        """

        self.images_folder = images_folder
        self.labels_folder = labels_folder

        self.dataset_train_df = self._read_csv(csv_train_path)

        if csv_val_path is not None:
            self.dataset_val_df = self._read_csv(csv_val_path)
            self.is_val_dataset = True
        else:
            print('No val dataset')
            self.is_val_dataset = False

        if csv_test_path is not None:    
            self.dataset_test_df = self._read_csv(csv_test_path)
            self.is_test_dataset = True
        else:
            print('No test dataset')
            self.is_test_dataset = False

        
    def _read_csv(self, csv_path):
        dataset_df = pd.read_csv(csv_path)
        return dataset_df

    # Make h5 group and write data
    def _write_data(self, h5py_file, width, height, dataset_type, dataset_df):
        """Prepare h5 file and write image data to it
        
        :param h5py_file: [h5 file to save]
        :type h5py_file: [h5py]
        :param width: [width of the image to save]
        :type width: [int]
        :param height: [height of the image to save]
        :type height: [int]
        :param dataset_type: [Pick dataset type (val/train/test)]
        :type dataset_type: [string]
        :param x_paths: [paths to images to save]
        :type x_paths: [string list]
        :param y_paths: [paths to labels to save]
        :type y_paths: [string list]
        """

        num_data = len(dataset_df)

        # h5py special data type for image.
        uint8_dt = h5py.special_dtype(vlen=np.dtype('uint8'))
        #h5py.special_dtype()
        # Make group and data set.
        group = h5py_file.create_group(dataset_type)
        x_dset = group.create_dataset('x', shape=(num_data, ), dtype=uint8_dt)
        y_dset = group.create_dataset('y', shape=(num_data, ), dtype=uint8_dt)
        #group.attrs.create(name='dataset_size', data=num_data, shape=None)
        group.create_dataset('dataset_size', data=num_data)

        for index, row in dataset_df.iterrows():
            # Read image and resize
            image_path = os.path.join(self.images_folder, row['images'])
            label_path = os.path.join(self.labels_folder, row['labels'])

            image = np.asarray(Image.open(image_path))
            image = cv2.resize(image, (width, height), fx=1, fy=1, interpolation=cv2.INTER_CUBIC) #512 256

            label = np.asarray(Image.open(label_path))
            label = cv2.resize(label, (width, height), fx=1, fy=1, interpolation=cv2.INTER_NEAREST)

            x_dset[index] = image.flatten()
            y_dset[index] = label.flatten()


    # Make h5 file.
    def make_h5py(self, h5_output_path, output_width, output_height):
        """Save prepared h5 file 
        
        :param saved_File_Name: [h5 file name]
        :type saved_File_Name: [string]
        :param destination_path: [file destination path]
        :param destination_path: str
        """

        # Make h5py file with write option.
        h5py_file = h5py.File(h5_output_path, 'w')

        # Write data
        print('Parsing train datas...')
        self._write_data(h5py_file, output_width, output_height, 'train', self.dataset_train_df)
        print('Finish.')

        if self.is_val_dataset:
            print('Parsing val datas...')
            self._write_data(h5py_file, output_width, output_height, 'val', self.dataset_val_df)
            print('Finish.')

        if self.is_test_dataset:
            print('Parsing test datas...')
            self._write_data(h5py_file, output_width, output_height, 'test', self.dataset_test_df)
            print('Finish.')
