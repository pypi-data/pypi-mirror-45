"""
Class used to evaluate prediction based on trained model from trainer module
"""

import json
import os
import time

import numpy as np
import pandas as pd
from keras import backend as K
from keras.models import load_model
from keras.optimizers import Adam
from scipy.ndimage import median_filter
from tqdm import tqdm
from PIL import Image

import cv2
import segmentation_module.segmentation_tools.generator_tools
from segmentation_module.segmentation_api.api_object import APIObject
from segmentation_module.segmentation_models.fcn import fcn_8s
from segmentation_module.segmentation_models.pspnet import pspnet50
from segmentation_module.segmentation_models.unet import unet
from segmentation_module.segmentation_tools.segmentation_tools import (get_model,
                                                                prepare_callbacks,
                                                                result_map_to_img,
                                                                result_map_to_raw_predict,
                                                                raw_2_blob,
                                                                save_any_img)
from segmentation_module.segmentation_tools.utils2 import (get_photos_from_dir,
                                                    make_folder_to_model,
                                                    prepare_folder_in_directory,
                                                    timed)



class Predictor(APIObject):

    __slots__ = ('model_path',
                'model',
                'input_width',
                'input_height',
                'n_classes',
                'output_path',
                'config_paths',
                'config_parameters',
                'config_classes',
                'config_colors',
                'predict_time',
                'logger',
                'model_folder')


    def __init__(self, config_dict, logger, config_path):
        super().__init__(config_dict)
        self.model_folder = os.path.dirname(config_path)
        self.logger = logger
        self.logger.log_message("PREDICTION STARTED")
        self._prepare_model_to_predict(self.config_parameters['model_name'])

    def get_pred_final_output_path(self):
        return self.output_path


    def _pick_model_type(self, model_name):

        model = get_model(model_name)
        return model


    def _prepare_model_to_predict(self, model_name):

        K.clear_session()

        #Get initial data
        self.n_classes = max(list(self.config_classes.values()))+1
        self.input_height = self.config_parameters['input_height']
        self.input_width = self.config_parameters['input_width']
        # self.path_to_weights = self.config_paths['path_to_weights']
        self.path_to_weights = os.path.join(self.model_folder, 'final_weights.h5')
        input_shape = (self.input_height, self.input_width, 3)

        model = self._pick_model_type(model_name)

        if(model):
            self.model = model(self.n_classes, input_shape, 1e-4, 5e-4)
        else:
            print("Select proper model type to prediction")

        self.model.load_weights(self.path_to_weights)
        self.logger.log_message('Weigths properly loaded.')
        

    def _filter_predition(self, image, kernel_size):
        img_filt = cv2.medianBlur(image, kernel_size)
        return img_filt

    def save_predictions(self, filenames, predictions, output_folder, model_name, methood='raw'):
        if methood == 'raw':
            pred_output_path = os.path.join(output_folder, 'predictions')
        elif methood == 'blobs':
            pred_output_path = os.path.join(output_folder, 'predictions_blobs')

        if not os.path.exists(pred_output_path):
	        os.makedirs(pred_output_path)

        for filename, pred in zip(filenames, predictions):
            if methood == 'raw':
                new_img_name = os.path.splitext(os.path.basename(filename))[0] + '_' + model_name + '.jpg'
            elif methood == 'blobs':
                new_img_name = os.path.splitext(os.path.basename(filename))[0] + '_' + model_name + '_blobs.jpg'
            new_path = os.path.join(pred_output_path, new_img_name)
            save_any_img(pred, new_path)

    def predict(self, images):
        predictions = []

        prediction_methood = 'raw'
        self.logger.log_message('Prediction output: {}'.format(prediction_methood))
        #Prepare folder to save predictions

        self.logger.log_message('Images to predict {}.'.format(len(images)))

        pred_only_time = 0

        for image in tqdm(images):

            raw_res, elapsed_time = self._predict_image(image)
            predictions.append(raw_res)
            pred_only_time += elapsed_time

        self.logger.log_message('Predict time for single photo: {:.1f}'.format(pred_only_time/len(images)))
        self.logger.log_message('FPS: {:.2f}'.format(1/(pred_only_time/len(images))))

        return np.array(predictions)


    def predict_dir(self, images_to_predict, output_path, only_to_memory=False):
        '''
        Predict images based on trained model

        Parameters:
        images_to predict: path to filder with images to predict
        output_path specyfied in config

        '''


        predictions = []
        # ! Only RAW supported!!!
        prediction_methood = 'raw'
        self.logger.log_message('Prediction output: {}'.format(prediction_methood))
        model_name = self.config_parameters['model_name']
        # colors = self.config_colors

        #Prepare folder to save predictions
        pred_output_path = os.path.join(output_path, 'predictions')

        if not os.path.exists(pred_output_path):
	        os.makedirs(pred_output_path)

        filenames = get_photos_from_dir(images_to_predict) 
        filenames.sort()

        self.logger.log_message('Images to predict {}.'.format(len(filenames)))

        pred_only_time = 0

        for filename in tqdm(filenames):

            raw_res, elapsed_time = self._predict_image(filename)
            predictions.append(raw_res)
            pred_only_time += elapsed_time

            new_img_name = os.path.splitext(os.path.basename(filename))[0] + '_' + model_name + '.jpg'
            new_path = os.path.join(pred_output_path, new_img_name)
            if not only_to_memory:
                save_any_img(raw_res, new_path)

        self.logger.log_message('Predict time for single photo: {:.1f}'.format(pred_only_time/len(filenames)))
        self.logger.log_message('FPS: {:.2f}'.format(1/(pred_only_time/len(filenames))))
        self.output_path = pred_output_path

        # TODO remove this keys from config file - no sense
        try:
            self.config_eval['raw_prediction_path'] = pred_output_path
            self.config_eval['eval_result_save_path'] = os.path.dirname(self.path_to_weights)
        except:
            print('No evaluator config in config file.')

        return np.array(predictions)

    def colorize_to_blobs(self, raw_preds, colors):
        blobs_list = []

        for raw_pred in raw_preds:
            blobs = raw_2_blob(raw_pred, colors)
            blobs_list.append(blobs)
            
        return blobs_list


    def predict_dir_deprecated(self, images_to_predict, output_path):
        '''
        Predict images based on trained model

        Parameters:
        images_to predict: path to filder with images to predict
        output_path specyfied in config

        '''

        prediction_methood = self.config_parameters['prediction_methood']
        self.logger.log_message('Prediction output: {}'.format(prediction_methood))
        model_name = self.config_parameters['model_name']
        colors = self.config_colors

        #Prepare folder to save predictions
        pred_output_path = os.path.join(output_path, 'predictions')

        if not os.path.exists(pred_output_path):
	        os.makedirs(pred_output_path)

        filenames = get_photos_from_dir(images_to_predict) 
        filenames.sort()

        self.logger.log_message('Images to predict {}.'.format(len(filenames)))

        pred_only_time = 0

        for filename in tqdm(filenames):

            raw_res, elapsed_time = self._predict_image(filename)
            pred_only_time += elapsed_time

            if prediction_methood == 'blobs':
                res = raw_2_blob(raw_res, colors)
            elif prediction_methood == 'raw':
                res = raw_res

            new_img_name = os.path.splitext(os.path.basename(filename))[0] + '_' + model_name + '.jpg'
            new_path = os.path.join(pred_output_path, new_img_name)
            save_any_img(res, new_path)

        self.logger.log_message('Predict time for single photo: {:.1f}'.format(pred_only_time/len(filenames)))
        self.logger.log_message('FPS: {:.2f}'.format(1/(pred_only_time/len(filenames))))
        self.output_path = pred_output_path

        try:
            self.config_eval['raw_prediction_path'] = pred_output_path
            self.config_eval['eval_result_save_path'] = os.path.dirname(self.path_to_weights)
        except:
            print('No evaluator config in config file.')

    def predict_image(self, path_to_image, output_path, only_to_memory=False):

        predictions = []
        # ! Only RAW supported!!!
        prediction_methood = 'raw'
        self.logger.log_message('Prediction output: {}'.format(prediction_methood))
        model_name = self.config_parameters['model_name']
        # colors = self.config_colors

        #Prepare folder to save predictions
        pred_output_path = os.path.join(output_path, 'predictions')

        if not os.path.exists(pred_output_path):
	        os.makedirs(pred_output_path)

        pred_only_time = 0


        raw_res, elapsed_time = self._predict_image(path_to_image)
        predictions.append(raw_res)
        pred_only_time += elapsed_time

        new_img_name = os.path.splitext(os.path.basename(path_to_image))[0] + '_' + model_name + '.jpg'
        new_path = os.path.join(pred_output_path, new_img_name)
        if not only_to_memory:
            save_any_img(raw_res, new_path)

        self.logger.log_message('Predict time for single photo: {:.1f}'.format(pred_only_time))
        self.logger.log_message('FPS: {:.2f}'.format(1/(pred_only_time)))
        self.output_path = pred_output_path

        # TODO remove this keys from config file - no sense
        try:
            self.config_eval['raw_prediction_path'] = pred_output_path
            self.config_eval['eval_result_save_path'] = os.path.dirname(self.path_to_weights)
        except:
            print('No evaluator config in config file.')

        return np.array(predictions)


    @timed
    def _predict_image(self, images):
    
        threshold = 0.5#self.config_parameters['confidence _threshold']

        images_adj = self._prepare_images_to_pred(images)

        pred = self.model.predict(images_adj)

        res = result_map_to_raw_predict(pred[0], self.input_height, self.input_width, threshold)

        return res

    def _prepare_images_to_pred(self, images):
        preprocessed_images = []
        if len(images.shape) == 3:
            images = np.expand_dims(images, axis=0)
        for image in images:
            image = Image.fromarray(image)
            image = image.resize((self.input_width, self.input_height))
            image = np.asarray(image)
            image = image / 127.5 - 1
            preprocessed_images.append(image)
        return np.asarray(preprocessed_images)

    # DEPRECATED: times are saved in log
    def report_prediction_time(self, n_images):
        time_data = []
        single_image_pred_time = self.predict_time / n_images
        pred_per_sec = 1 / single_image_pred_time
        time_data = [[single_image_pred_time], [pred_per_sec]]
        time_df = pd.DataFrame(time_data, columns = ["Time"], index=["Single image pred [s]: ","FPS: "])
        time_df.to_csv(os.path.join(self.output_path, "time.txt"), float_format='%.3f', sep=" ", index=True)