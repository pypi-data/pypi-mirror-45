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


class API(object):

    __slots__ = ('predictor',
                 'config_manager',
                 'logger')

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
        model_path = trainer.model_path
        self.logger.move_file(config_dict['paths']['original_model_path'])
        self.config_manager.save_json(new_config_dict, model_path)

    def train_and_predict_and_vis(self, config_path, images_to_predict_path, vis_output_path):
        """Function respinsible for training model, predict images on trained model and visualize predictions
        
        :param config_path: path to configuration file
        :type config_path: [string]
        :param images_to_predict_path: [path to images to predict]
        :type images_to_predict_path: [string]
        :param vis_output_path: [path to output folder]
        :type vis_output_path: [string]
        """

        config_dict = self.config_manager.get_config(config_path)

        trainer = Trainer(config_dict, self.logger)
        # start training
        trainer.train()

        new_config_dict = trainer.get_config_dict()
        model_path = trainer.model_path

        #Start predictions
        predictor = Predictor(new_config_dict, self.logger)
        predictor.predict_dir(images_to_predict_path, vis_output_path,)
        prediction_path = predictor.get_pred_final_output_path()

        #Visualize predictions
        visualizer = Visualizator(new_config_dict, self.logger)
        visualizer.visualize_folder(images_to_predict_path, prediction_path, vis_output_path)

        self.logger.move_file(config_dict['paths']['original_model_path'])
        self.config_manager.save_json(new_config_dict, model_path)


    def predict_and_visualize(self, config_path, images_to_predict_path, vis_output_path):
        """Predict and visualize images based on trained model specyfied in config file
        
        :param config_path: path to configuration file
        :type config_path: [string]
        :param images_to_predict_path: path to folder with images to predict
        :type images_to_predict_path: [string]
        :param vis_output_path: path to output folder to prediction visualisation
        :type vis_output_path: [string]
        :param mode: 'blobs' or 'raw', default to 'raw'
        :param mode: str, optional
        """
        config_dict = self.config_manager.get_config(config_path)

       #Start predictions
        predictor = Predictor(config_dict, self.logger)
        predictor.predict_dir(images_to_predict_path, vis_output_path)
        prediction_path = predictor.get_pred_final_output_path()

        #Visualize predictions
        visualizer = Visualizator(config_dict, self.logger)
        visualizer.visualize_folder(images_to_predict_path, prediction_path, vis_output_path, transparent_ratio=0.4)


    def visualize(self, config_path, images_to_predict_path, prediction_path, vis_output_path):
        """Visualize raw prediction
        
        :param config_path: path to configuration file
        :type config_path: [string]
        :param images_to_predict_path: path to folder with images
        :type images_to_predict_path: [string]
        :param prediction_path: path to folder with predicted images
        :type prediction_path: [string]
        :param vis_output_path: path to visualisation output folder
        :type vis_output_path: [string]
        """

        config_dict = self.config_manager.get_config(config_path)

        #Visualize predictions
        visualizer = Visualizator(config_dict, self.logger)
        visualizer.visualize_folder(images_to_predict_path, prediction_path, vis_output_path, transparent_ratio=0.4)


    def visualize_image(self, config_path, orig_image_path, pred_image_path):
        """Visualize raw prediction
        
        :param config_path: path to configuration file
        :type config_path: [string]
        :param images_to_predict_path: path to folder with images
        :type images_to_predict_path: [string]
        :param prediction_path: path to folder with predicted images
        :type prediction_path: [string]
        :param vis_output_path: path to visualisation output folder
        :type vis_output_path: [string]
        """

        config_dict = self.config_manager.get_config(config_path)

        #Visualize predictions
        visualizer = Visualizator(config_dict, self.logger)
        vis_result = visualizer.visualize_single_image(orig_image_path, pred_image_path, transparent_ratio=0.4)

        return vis_result

    def predict_and_visualize_image(self, config_path, orig_image_path):
        """Visualize raw prediction
        
        :param config_path: path to configuration file
        :type config_path: [string]
        :param images_to_predict_path: path to folder with images
        :type images_to_predict_path: [string]
        :param prediction_path: path to folder with predicted images
        :type prediction_path: [string]
        :param vis_output_path: path to visualisation output folder
        :type vis_output_path: [string]
        """

        config_dict = self.config_manager.get_config(config_path)
    
        if self.predictor is None:
            predictor = Predictor(config_dict, self.logger)

        pred_result, _ = predictor.predict_image(orig_image_path)
        pred_blob = raw_2_blob(pred_result, config_dict["colors"])
        #Visualize predictions
        visualizer = Visualizator(config_dict, self.logger)
        vis_result = visualizer.visualize_single_image(orig_image_path, pred_blob, transparent_ratio=0.8)

        return pred_result, vis_result, pred_blob

    def predict__(self, config_path, images_to_predict, output_folder):
        config_dict = self.config_manager.get_config(config_path)
        predictor = Predictor(config_dict, self.logger, config_path)

        if os.path.isdir(images_to_predict):
            result = predictor.predict_dir(images_to_predict, output_folder)
        else:
            result = predictor.predict_image(images_to_predict, output_folder)


    def predict_deprecated(self, config_path, images_to_predict_path, vis_output_path, predict_methood):
        """Predict images based on trained model specyfied in config

        :param config_path: path to configuration file
        :type config_path: [string]
        :param images_to_predict_path: path to folder with images
        :type images_to_predict_path: [string]
        :param vis_output_path:  path to visualisation output folder
        :type vis_output_path: [string]
        :param predict_methood: type of images to save after prediction "blobs" or "raw"
        :type predict_methood: [string]
        """
        config_dict = self.config_manager.get_config(config_path)

         #Start predictions
        predictor = Predictor(config_dict, self.logger)
        predictor.predict_dir(images_to_predict_path, vis_output_path)
        
    def predict_image_deprecated(self, config_path, images_to_predict_path, pred_output_path, predict_methood):
        """[summary]
        
        :param config_path: [description]
        :type config_path: [type]
        :param images_to_predict_path: [description]
        :type images_to_predict_path: [type]
        :param vis_output_path: [description]
        :type vis_output_path: [type]
        :param predict_methood: [description]
        :type predict_methood: [type]
        """
        config_dict = self.config_manager.get_config(config_path)

        if self.predictor is None:
            predictor = Predictor(config_dict, self.logger)

        result = predictor.predict_image(images_to_predict_path)
        return result


    def overall_training(self, config_path, images_to_predict_path, vis_output_path):
        """[summary]
        
        :param config_path: [description]
        :type config_path: [type]
        :param images_to_predict_path: [description]
        :type images_to_predict_path: [type]
        :param vis_output_path: [description]
        :type vis_output_path: [type]
        """

        config_dict = self.config_manager.get_config(config_path)
        config_dict = prepare_to_train(config_dict)

        trainer = Trainer(config_dict, self.logger)
        # start training
        trainer.train()

        new_config_dict = trainer.config_dict
        model_path = trainer.model_path

        #Start predictions
        predictor = Predictor(new_config_dict, self.logger)
        predictor.predict_dir(images_to_predict_path, vis_output_path)
        prediction_path = predictor.get_pred_final_output_path()

        #Visualize predictions
        visualizer = Visualizator(new_config_dict, self.logger)
        visualizer.visualize_folder(images_to_predict_path, prediction_path, vis_output_path)

        new_config_dict['evaluator']['raw_prediction_path'] = prediction_path

        evaluator = Evaluator(new_config_dict, self.logger)
        evaluator.calculate_evaluation_metrics()
        evaluator.save_evaluation_table()

        self.logger.move_file(config_dict['paths']['original_model_path'])
        self.config_manager.save_json(new_config_dict, model_path)

    def train_and_predict_and_evaluate(self, config_path, images_to_predict_path, vis_output_path):
        """Congeneric method responsible for training model, predict images and evaluation
        
        :param config_path: path to configuration file
        :type config_path: [string]
        :param images_to_predict_path: path to folder with images to predict
        :type images_to_predict_path: [string]
        :param vis_output_path: path to visualisation output path
        :type vis_output_path: [string]
        """

        config_dict = self.config_manager.get_config(config_path)

        trainer = Trainer(config_dict, self.logger)
        # start training
        trainer.train()

        new_config_dict = trainer.config_dict
        model_path = trainer.model_path

        #Start predictions
        predictor = Predictor(new_config_dict, self.logger)
        predictor.predict_dir(images_to_predict_path, vis_output_path)
        prediction_path = predictor.get_pred_final_output_path()
        
        evaluator = Evaluator(new_config_dict, self.logger)
        evaluator._prepare_data()
        evaluator.calculate_mean_precision_recall()
        evaluator.calculate_mean_pixel_accuracy()
        evaluator.calculate_mean_iou()
        evaluator.save_evaluation_table()

        self.logger.move_file(config_dict['paths']['original_model_path'])
        self.config_manager.save_json(new_config_dict, model_path)

    def evaluate(self, config_path):
        """Evaluate model based on prediction

        :param config_path: path to configuration file
        :type config_path: [string]
        """
        config_dict = self.config_manager.get_config(config_path)

        evaluator = Evaluator(config_dict, self.logger)
        evaluator.calculate_evaluation_metrics()
        evaluator.save_evaluation_table()
