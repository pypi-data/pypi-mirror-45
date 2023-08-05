
'''
Utilities module responsible for additional useful methoods for training, visualisation or prediction
'''

import os
import cv2
from PIL import Image

import numpy as np
from keras.callbacks import (EarlyStopping, LearningRateScheduler,
                             ModelCheckpoint, ReduceLROnPlateau, TensorBoard)

from keras.callbacks import Callback

from segmentation_module.segmentation_models.fcn import fcn_8s
from segmentation_module.segmentation_models.pspnet import pspnet50
from segmentation_module.segmentation_models.unet import unet

class TrainCheck(Callback):
    def __init__(self, img_2_vis_paths, output_path, model_name, colors, input_height, input_width):
        self.epoch = 0
        self.img_2_vis_paths = img_2_vis_paths
        self.output_path = output_path
        self.model_name = model_name
        self.colors = colors
        self.input_height = input_height
        self.input_width = input_width

    def result_map_to_img(self, res_map, colors):
        img = np.zeros((self.input_height, self.input_width, 3), dtype=np.uint8)
        res_map = np.squeeze(res_map)

        argmax_idx = np.argmax(res_map, axis=2)
        
        for i, (key, color) in enumerate(colors.items()):
            color = color[::-1]

            img[argmax_idx == i] = color # i+1 because of background
            indx, indy = np.nonzero(argmax_idx == i)
            #print("{}: {}".format(key, len(indx)))

        return img

    def on_epoch_end(self, epoch, logs={}):
        self.epoch = epoch+1
        for img_path in self.img_2_vis_paths:
            try:
                self.visualize(img_path)
            except:
                print('Cannot visualized {}.'.format(img_path))
        # self.visualize(test_img3_path)
        # self.visualize('img/DJI_0157_orig.png')
        # self.visualize('img/DJI_0181_orig.png')

    def visualize(self, path):
        img = cv2.imread(path)
        img = cv2.resize(img, (self.input_width, self.input_height))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 127.5 - 1
        img = np.expand_dims(img, 0)

        pred = self.model.predict(img)
        #pdb.set_trace()
        colors = self.colors
        res_img = self.result_map_to_img(pred[0], colors)

        img_name = os.path.split(path)[-1]
        cv2.imwrite(os.path.join(self.output_path, img_name[:-4] + self.model_name + '_epoch_' + str(self.epoch) +'_NEW' + '.png'), res_img)


def get_model(model_name):
    
    model_set = {         
        'fcn': fcn_8s,
        'unet': unet,
        'pspnet': pspnet50
    }

    model = model_set[model_name]
    return model

def prepare_callbacks(path_to_model, config_parameters, config_colors, config_path):

    input_width = config_parameters['input_width']
    input_height = config_parameters['input_height']
    train_batch_size = config_parameters['train_batch_size']
    monitor_parameter = config_parameters['quantity_parameter']
    patience = config_parameters['patience']
    model_name = config_parameters['model_name']
    img_2_vis_paths = config_path['img_2_vis_paths']

    if monitor_parameter == 'val_dice_coef':
        mode = 'max'
    else:
        mode = 'auto'

    path_to_log = os.path.join(path_to_model, 'log')
    os.makedirs(path_to_log)

    # CALLBACKS:
    model_checkpoint = ModelCheckpoint(filepath=os.path.join(path_to_model,
                                                model_name + '_weights_epoch-{epoch:02d}_loss-{loss:.4f}_val_loss-{val_loss:.4f}.h5'),
                                    monitor=monitor_parameter, # mark as parameter default val_loss
                                    verbose=1,
                                    save_best_only=True,
                                    save_weights_only=True,
                                    mode=mode,
                                    period=1)
    
    tensorboard_logger = TensorBoard(log_dir= path_to_log, 
                                    histogram_freq=0, 
                                    batch_size=train_batch_size, 
                                    write_graph=True, 
                                    write_grads=True, 
                                    write_images=True)

    learning_rate_scheduler = LearningRateScheduler(lr_schedule)

    early_stopping = EarlyStopping(monitor=monitor_parameter,
                                   min_delta=0.001,
                                   patience=patience,
                                   mode=mode)

    reduce_lr = ReduceLROnPlateau(monitor='val_loss', 
                                  factor=0.1, 
                                  patience=5, 
                                  min_lr=0.00001)

    train_check = TrainCheck(img_2_vis_paths, path_to_model, model_name, config_colors, input_height, input_width)


    callbacks = [model_checkpoint, tensorboard_logger, train_check, learning_rate_scheduler, early_stopping, reduce_lr]

    return callbacks


def lr_schedule(epoch):
    if epoch < 10:
        return 0.001
    elif epoch < 25:
        return 0.0001
    else:
        return 0.00001

def result_map_to_img(res_map, colors, input_height, input_width, threshold):
    img = np.zeros((input_height, input_width, 3), dtype=np.uint8) # DEPRESYJNA CZERN
    res_map = np.squeeze(res_map)
    # Extract pixel pred where probabiliti is greatear than threshold
    res_map_new = np.where(res_map > threshold, res_map, 0)
    argmax_idx = np.argmax(res_map_new, axis=2)
    
    for i, (key, color) in enumerate(colors.items()):
        color = color[::-1]
        img[argmax_idx == i] = color

    return img

def raw_2_blob(raw_pred, colors):
    #img = np.zeros((input_height, input_width, 3), dtype=np.uint8) # DEPRESYJNA CZERN
    img = np.zeros_like(raw_pred, dtype=np.uint8)

    if len(raw_pred.shape) == 3:
        raw_pred = raw_pred[:, :, 0]

    for i, (key, color) in enumerate(colors.items()):
        img[raw_pred == i] = color

    return img

def save_any_img(image, output_path):
    image_to_save = Image.fromarray(np.uint8(image))
    new_image_path = os.path.splitext(output_path)[0] + '.png'
    image_to_save.save(new_image_path)

def result_map_to_raw_predict(res_map, input_height, input_width, threshold):

    img = np.zeros((input_height, input_width, 3), dtype=np.uint8) # DEPRESYJNA CZERN
    res_map = np.squeeze(res_map)  
    # Extract pixel pred where probabiliti is greatear than threshold
    res_map_new = np.where(res_map > threshold, res_map, 0)
    argmax_idx = np.argmax(res_map_new, axis=2)

    img = np.stack([argmax_idx, argmax_idx, argmax_idx], axis=2)

    return img

def map_label_2_sandwich(img, classes_dict, width, height):

	classes_no = max(list(classes_dict.values()))+1

	y_img = np.reshape(img, ( height, width))
	result_map = np.zeros((height, width, classes_no))

	for i, (_, item) in enumerate(classes_dict.items()):
		y_img[y_img==i] = item

	for class_no in range(1, classes_no):
		result_map[:, :, class_no] = np.where((y_img == class_no), 1, 0)

	not_background_new = np.sum(result_map, axis=2)

	background_new = np.logical_not(not_background_new)
	result_map[:, :, 0] = np.where(background_new, 1, 0)

	return result_map