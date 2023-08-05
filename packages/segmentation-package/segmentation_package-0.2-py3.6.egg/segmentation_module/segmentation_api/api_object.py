import json
import os

class APIObject():
    def __init__(self, config):
        """[summary]
        
        :param config: [description]
        :type config: dictionary with configs
        """
        try:    
            self.config_paths = config['paths']
        except:
            print('Cannot read Paths.')

        try:  
            self.config_parameters = config['parameters']
        except:
            print('Cannot read parameters.')
        
        try:  
            self.config_classes = config['classes']
        except:
            print('Cannot read classes_descriptions.')        

        try:    
             self.config_colors = config['colors']
        except:
            print('Cannot read colors.')
        
        try:
            self.config_eval = config['evaluator']
        except:
            print('Cannot read evaluator.')        
        
        try:
            self.config_classes_desc = config['classes_descriptions']
        except:
            print('Cannot read classes.')

    def create_config_dict(self):
        config_dict = {
                        'paths' : self.config_paths,
                        'parameters' : self.config_parameters,
                        'classes_descriptions' : self.config_classes_desc,
                        'colors' : self.config_colors,
                        'evaluator' : self.config_eval,
                        'classes' : self.config_classes
                      }
        return config_dict

"""
    Class resposnsible for loading, writing and managing config files.
"""

class ConfigCEO():

    __slots__: ('config')

    def __init__(self):
        pass

    def save_json(self, config_dict, model_path):
        save_path = os.path.join(model_path, 'config_model.json')    

        with open(save_path, 'w') as out_file:
            json.dump(config_dict, out_file, indent=4)

    def get_config(self, config_path):
        with open(config_path) as json_file:   
            config_dict = json.load(json_file)
        return config_dict

    def set_paramater(self, config_dict, group, parameter, new_value):
        config_dict[group][parameter] = new_value
        return config_dict