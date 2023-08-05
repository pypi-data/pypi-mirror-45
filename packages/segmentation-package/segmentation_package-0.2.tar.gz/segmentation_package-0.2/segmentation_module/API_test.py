from segmentation_module.segmentation_api.API import API

config_path = r"configs\config_model_KS.json"
config_path = r"configs\config_stitch.json"

api = API()
#api.train_model(config_path)

config_path = r"C:\Users\PR\OneDrive_Politechnika_Warszawska\Repositories\segmentation_module\configs\config_stitch.json"
img_path = r"C:\Users\PR\GISS\Stitch_dataset\images\val\image_0002.png"
img_folder = r"D:\segmentation_labels_15_04_2019\images\val"
img_path = r"F:\GISS\Gildia_kupiecka\Google_Drive\GISS\Data\2019-04-09_original_deg0_100m_fort_bema\images\raw_images\DJI_0003.JPG"
outputo = r"F:\GISS\Gildia_kupiecka\stitch"

# api.predict_and_visualize(config_path, img_path, outputo, with_blobs=True)

#api.predict(config_path, img_folder, 'example_preds6')

#predictions_path = r"example_preds3\predictions"
#api.visualize(config_path, img_folder, predictions_path, 'example_preds3')

#api.predict_and_visualize(config_path, img_folder, 'example_preds4')


#api.train_and_predict_and_visualize(config_path, img_folder, with_blobs=True)

# config_eval = r"configs\config_eval_segmentation.json"
# predictions_folder_path = r"C:\\Users\\PR\\Desktop\\Paths_prediction\\Stitche\\labels_stitch_3\\annotations"
# labels_folder_path = r"C:\\Users\\PR\\Desktop\\Paths_prediction\\Stitche\\labels_stitch_3\\annotations"
    
# api.evaluate(config_eval, predictions_folder_path, labels_folder_path)


config_path = r"C:\Users\PR\Documents\segmentation_training\unet_2019-04-15-13-50-57\config_model.json"
api.predict_and_visualize(config_path, img_path, 'example_preds4', with_blobs=True)