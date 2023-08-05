"""
Class for performing model training based on given data and config
"""

import json
import os
from shutil import copyfile

import numpy as np
import pandas as pd
from keras import backend as K
from keras.optimizers import Adam

from segmentation_module.segmentation_api.api_object import APIObject
# from Models.models import FCN32, FCN8, VGGUnet, VGGUnet_orig, Segnet, Unet, FCN_Vgg16_32s, fcn_8s_NEW 
from segmentation_module.segmentation_tools.generator_tools import \
    prepare_generators_adapt
from segmentation_module.segmentation_tools.segmentation_tools import \
    prepare_callbacks, get_model
from segmentation_module.segmentation_tools.utils2 import (cleaning_weights_in_folder,
                                                    make_folder_to_model)


class Trainer(APIObject):
    
    __slots__ = ('config_paths',
                'config_parameters',
                'config_classes',
                'config_colors',
                'model',
                'path_to_saved_model',
                'config_path',
                'config_dict',
                'model_path')

    def __init__(self, config_path, logger):
        super().__init__(config_path)
        self.logger = logger
        self.logger.log_message('TRAINING STARTED.')
        
    def train(self):
        '''
        Train selected model TBD..

        '''
        K.clear_session()
        self.logger.log_message("TF session cleared.")

        #validate = self.config['validate']
        model_path = self.config_paths['original_model_path']
        epochs = self.config_parameters['epochs']

        model_name = self.config_parameters['model_name']

        self.model_path = model_path

        self._prepare_model(model_name)
        
        self.logger.log_message("Model architecture: {}".format(model_name))
        self.logger.log_message("Model output shape: {}".format(self.model.output_shape))
        self.logger.log_message("Number of epochs: {}".format(epochs))

        train_gen, val_gen, steps_per_train_epoch, steps_per_val_epoch = prepare_generators_adapt(self.config_parameters, self.config_paths, self.config_classes)

        self.logger.log_message("Steps per train epoch: {}".format(steps_per_train_epoch))
        self.logger.log_message("Steps per val epoch: {}".format(steps_per_val_epoch))
        
        callbacks = prepare_callbacks(model_path, 
                                      self.config_parameters, 
                                      self.config_colors,
                                      self.config_paths)

        self.model.fit_generator(generator=train_gen,
                            steps_per_epoch=steps_per_train_epoch,
                            epochs=epochs,
                            callbacks=callbacks,
                            validation_data=val_gen,
                            validation_steps=steps_per_val_epoch)

        self.save_training_history()       

        final_weights_path = cleaning_weights_in_folder(model_path)
        final_model_path = os.path.join(model_path, ("final_model.h5"))

        self.model.save_weights(final_weights_path)
        self.logger.log_message("Weights saved.")

        if self.config_parameters["save_model"]:
            self.model.load_weights(final_weights_path)
            self.model.save(final_model_path)
            self.logger.log_message("Model saved.")

        self.config_paths['path_to_weights'] = final_weights_path
        self.config_dict = super().create_config_dict()

    def save_training_history(self):

        history_path = os.path.join(self.model_path, "history.csv")
        pd.DataFrame(self.model.history.history).to_csv(history_path)
        self.logger.log_message("Training history saved")

    def _pick_model_type(self, model_name):
        model = get_model(model_name)
        return model

    def get_config_dict(self):
        return self.config_dict

    def _prepare_model(self, model_name):

        num_classes  = max(list(self.config_classes.values()))+1
        input_height = self.config_parameters['input_height']
        input_width = self.config_parameters['input_width']
        learning_rate = self.config_parameters['learning_rate']
        input_shape = (input_height, input_width, 3)
        vgg_weight_path = self.config_paths['VGG_Weights_path']

        model = self._pick_model_type(model_name)

        if model_name == 'pspnet':
            self.model = model(num_classes, input_shape, learning_rate, 5e-4)
        else:
            self.model = model(num_classes, input_shape, learning_rate, 5e-4, vgg_weight_path)
