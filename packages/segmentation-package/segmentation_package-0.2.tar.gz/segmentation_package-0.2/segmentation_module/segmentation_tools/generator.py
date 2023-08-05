'''
Module adapted from image-segmentation-keras to check training 
'''

import random
from random import randint, uniform

import h5py
import numpy as np
from keras.preprocessing.image import ImageDataGenerator

import cv2
from segmentation_module.segmentation_tools.segmentation_tools import \
    map_label_2_sandwich


def pre_processing(img):
    # Random exposure and saturation (0.9 ~ 1.1 scale)
    rand_s = random.uniform(0.9, 1.1)
    rand_v = random.uniform(0.9, 1.1)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    tmp = np.ones_like(img[:, :, 1]) * 255
    img[:, :, 1] = np.where(img[:, :, 1] * rand_s > 255, tmp, img[:, :, 1] * rand_s)
    img[:, :, 2] = np.where(img[:, :, 2] * rand_v > 255, tmp, img[:, :, 2] * rand_v)

    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)

    # Centering helps normalization image (-1 ~ 1 value)
    return img / 127.5 - 1

def pre_processing_val(img):
    return img / 127.5 - 1

#Adapted from Data agumentator made by PR  HSV manipulations-> to simulate different seasons.

# Get ImageDataGenerator arguments(options) depends on mode - (train, val, test)
# Generate argumenrs for Keras data agumentation
def get_data_gen_args(mode):
    if mode == 'train':

        base_dict = dict(shear_range=0.5,
                         zoom_range=0.5,
                         rotation_range=180,
                         width_shift_range=0.5,
                         height_shift_range=0.5,
                         fill_mode='constant',
                         horizontal_flip=True)

        x_data_gen_args = base_dict.copy()
        x_data_gen_args.update(preprocessing_function=pre_processing) #was pre_processing
        
        y_data_gen_args = base_dict
    elif mode == 'test' or mode == 'val':
        x_data_gen_args = dict(preprocessing_function=pre_processing_val)#dict(preprocessing_function=pre_processing)
        y_data_gen_args = dict()

    else:
        print("Data_generator function should get mode arg 'train' or 'val' or 'test'.")
        return -1

    return x_data_gen_args, y_data_gen_args


# One hot encoding for y_img.
def get_sandwich(y_imgs, input_height, input_width, classes_dict):

    batch_result = []

    for y_img in y_imgs:

        result_map = map_label_2_sandwich(y_img, classes_dict, input_width, input_height)
        batch_result.append(result_map)

    batch_result = np.array(batch_result)
    return batch_result

def read_h5(h5_path):
    data = h5py.File(h5_path, 'r')

    x_train = data.get('/train/x')
    y_train = data.get('/train/y')
    x_val = data.get('/val/x')
    y_val = data.get('/val/y')
    train_dataset_size = data.get('/train/dataset_size').value
    val_dataset_size = data.get('/val/dataset_size').value

    return x_train, y_train, x_val, y_val, train_dataset_size, val_dataset_size


# Data generator for fit_generator.
def data_generator(x_imgs, y_imgs, input_height, input_width, classes_dict, batch_size, mode):

    # Make ImageDataGenerator.

    x_data_gen_args, y_data_gen_args = get_data_gen_args(mode)
    x_data_gen = ImageDataGenerator(**x_data_gen_args)
    y_data_gen = ImageDataGenerator(**y_data_gen_args)
    
    # random index for random data access.
    d_size = x_imgs.shape[0]
    shuffled_idx = list(range(d_size))

    x = []
    y = []
    while True:
        random.shuffle(shuffled_idx)
        for i in range(d_size):
            idx = shuffled_idx[i]

            x.append(x_imgs[idx].reshape((input_height, input_width, 3)))
            y.append(y_imgs[idx].reshape((input_height, input_width, 1)))

            if len(x) == batch_size:
                # Adapt ImageDataGenerator flow method for data augmentation.
                _ = np.zeros(batch_size)
                seed = random.randrange(1, 1000)

                x_tmp_gen = x_data_gen.flow(np.array(x), _,
                                            batch_size=batch_size,
                                            seed=seed)
                y_tmp_gen = y_data_gen.flow(np.array(y), _,
                                            batch_size=batch_size,
                                            seed=seed)

                # Finally, yield x, y data.
                x_result, _ = next(x_tmp_gen)
                y_result, _ = next(y_tmp_gen)
                sandwich = get_sandwich(y_result, input_height, input_width, classes_dict)
                yield x_result, sandwich

                x.clear()
                y.clear()
