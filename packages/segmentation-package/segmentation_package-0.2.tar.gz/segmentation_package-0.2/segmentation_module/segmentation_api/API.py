'''
Class for managing functionality of semantic segmentation model solution.
'''

from segmentation_module.segmentation_api.api_object import ConfigCEO
from segmentation_module.segmentation_api.evaluator import Evaluator
from segmentation_module.segmentation_api.logger import Logger
from segmentation_module.segmentation_api.predictor import Predictor
from segmentation_module.segmentation_api.trainer import Trainer
from segmentation_module.segmentation_api.visualizator import Visualizator
from segmentation_module.segmentation_tools.utils2 import (make_folder_to_model,
                                                    prepare_to_train)
from segmentation_module.segmentation_tools.segmentation_tools import raw_2_blob

import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = 100000000000000      
import numpy as np
from segmentation_module.segmentation_tools.utils2 import get_photos_from_dir

def load_images_batch(images_path, output_resolution=None):
    images_batch = []

    if os.path.isdir(images_path):
        filenames = get_photos_from_dir(images_path)
    else:
        filenames = [images_path]

    for image_path in filenames:
        image = Image.open(image_path)
        if output_resolution is not None:
            image = image.resize(output_resolution)
        images_batch.append(np.asarray(image))
    images_batch = np.asarray(images_batch)
    return images_batch, filenames

class API(object):

    __slots__ = ('predictor',
                 'config_manager',
                 'logger',
                 'model_path')

    def __init__(self):
        self.predictor = None
        self.config_manager = ConfigCEO()
        self.logger = Logger(r'temp\segmentation_logger.log')

    def train_model(self, config_path):
        """Function responsible for training model based on parameters in config
        
        :param config_path: path to configuration file
        :type config_path: [string]
        """

        config_dict = self.config_manager.get_config(config_path)
        config_dict = prepare_to_train(config_dict)

        trainer = Trainer(config_dict, self.logger)
        # start training
        trainer.train()

        new_config_dict = trainer.get_config_dict()
        self.model_path = trainer.model_path
        self.logger.move_file(config_dict['paths']['original_model_path'])
        self.config_manager.save_json(new_config_dict, self.model_path)

    def predict(self, config_path, images_path, output_folder, only_to_memory=False, with_blobs=False):
        config_dict = self.config_manager.get_config(config_path)
        predictor = Predictor(config_dict, self.logger, config_path)

        resolution = (config_dict['parameters']['input_width'],
                      config_dict['parameters']['input_height'])

        images, filenames = load_images_batch(images_path, resolution)
        predictions = predictor.predict(images)
        if with_blobs:
            predictions_blobs = predictor.colorize_to_blobs(predictions, config_dict['colors'])

        if not only_to_memory:
            predictor.save_predictions(filenames, predictions, output_folder, config_dict['parameters']['model_name'])
            if with_blobs:
                predictor.save_predictions(filenames, predictions_blobs, output_folder, config_dict['parameters']['model_name'], methood='blobs')

        if with_blobs:
            return predictions, predictions_blobs
        else:
            return predictions

    def visualize(self, config_path, images_path, predictions_path, output_folder, only_to_memory=False):
        config_dict = self.config_manager.get_config(config_path)
        visualizer = Visualizator(config_dict, self.logger)

        resolution = (config_dict['parameters']['input_width'],
                      config_dict['parameters']['input_height'])

        images, images_filenames = load_images_batch(images_path, resolution)
        preds, preds_filenames = load_images_batch(predictions_path, resolution)

        visualizations = visualizer.visualize(images, preds, transparent_ratio=0.4)
        
        if not only_to_memory:
            visualizer.save_visualizations(images_filenames, visualizations, output_folder, config_dict['parameters']['model_name'])

        return visualizations

    def predict_and_visualize(self, config_path, images_to_predict, output_folder, only_to_memory=False, with_blobs=False):
        config_dict = self.config_manager.get_config(config_path)
        predictor = Predictor(config_dict, self.logger, config_path)
        visualizer = Visualizator(config_dict, self.logger)
        resolution = (config_dict['parameters']['input_width'],
                      config_dict['parameters']['input_height'])

        images, filenames = load_images_batch(images_to_predict, resolution)
        predictions = predictor.predict(images)
        if with_blobs:
            predictions_blobs = predictor.colorize_to_blobs(predictions, config_dict['colors'])
        visualizations = visualizer.visualize(images, predictions, transparent_ratio=0.4)

        if not only_to_memory:
            predictor.save_predictions(filenames, predictions, output_folder, config_dict['parameters']['model_name'])
            if with_blobs:
                predictor.save_predictions(filenames, predictions_blobs, output_folder, config_dict['parameters']['model_name'], methood='blobs')
            visualizer.save_visualizations(filenames, visualizations, output_folder, config_dict['parameters']['model_name'])

        if with_blobs:
            return predictions, predictions_blobs, visualizations
        else:
            return predictions, visualizations

    def train_and_predict_and_visualize(self, config_path, images_to_predict, only_to_memory=False, with_blobs=False):
        self.train_model(config_path)
        new_config_path = os.path.join(self.model_path, 'config_model.json')
        output = self.predict_and_visualize(new_config_path, images_to_predict, self.model_path, only_to_memory, with_blobs)
        return output

    def evaluate(self, config_path, predictions_folder_path, labels_folder_path):
        """Evaluate model based on prediction

        :param config_path: path to configuration file
        :type config_path: [string]
        """
        config_dict = self.config_manager.get_config(config_path)

        evaluator = Evaluator(config_dict, self.logger)
        evaluator.load_data(predictions_folder_path, labels_folder_path)
        evaluator.calculate_evaluation_metrics()
        evaluator.save_evaluation_table()

    