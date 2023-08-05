import glob
import itertools
import os

import h5py
import numpy as np
import PIL.Image as Image
from tqdm import tqdm, trange

import cv2
#from DataAugmentator import DataAugmentator
from segmentation_module.segmentation_tools.generator import data_generator, read_h5
from segmentation_module.segmentation_tools.segmentation_tools import \
    map_label_2_sandwich
from segmentation_module.segmentation_tools.utils2 import get_photos_from_dir


def read_img(filename, width , height):
	img = cv2.imread(filename, 1)
	img = cv2.resize(img, (width, height))
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	#img = img.astype(np.float32)
	return img

def normalize_img(img, operations=['subtract_mean', 'divide']):
	if 'divide' in operations:
		divider = 255.0
	else:
		divider = 1
	if 'subtract_mean' in operations:
		img = img/divider
		img[:,:,0] -= 103.939/divider
		img[:,:,1] -= 116.779/divider
		img[:,:,2] -= 123.68/divider
	return img

class DataGenerator(object):
#TODO asymilate reading images from h5 file in this class to create generators
	def __init__(self, images_path, segs_path, width, height, nClasses, is_h5 = False, h5_path ="", dataset_type =""): #TODO bad design think of sth better later
		
		#TODO read from csv, get only images with corresponding labels
		images = get_photos_from_dir(images_path)
		images.sort()
		labels = get_photos_from_dir(segs_path)
		labels.sort()
	
		self.width = width
		self.height	= height
		self.nClasses = nClasses

		assert len(images) == len(labels)
		self.dataset_size = len(images)
		
		perm = np.random.permutation(self.dataset_size)
		
		images = np.array(images)[perm]
		labels = np.array(labels)[perm]

		if is_h5:			
			print('Starting reading images.')
			images = self._read_img_from_h5_file(h5_path, self.width , self.height, dataset_type, 'img')
			print('Loaded {} images to generator.'.format(len(images)))
			print('Starting reading labels.')
			labels = self._read_img_from_h5_file(h5_path, self.width , self.height, dataset_type, 'labels')
			print('Loaded {} labels to generator.'.format(len(labels)))    
		else:
			print('Starting reading images.')
			images = self._read_imgs_to_numpy(images, self.width , self.height)
			print('Loaded {} images to generator.'.format(len(images)))
			print('Starting reading labels.')
			labels = self._read_labels_to_numpy(labels, self.width , self.height, nClasses)
			print('Loaded {} labels to generator.'.format(len(labels)))

		self.zipped = itertools.cycle( zip(images, labels))
        
	
	def _read_labels_to_numpy(self, filenames, width , height, nClasses):
		labels = []
		for filename in tqdm(filenames):
			label_img = np.asarray(Image.open(filename))
			labels.append(label_img)
		labels = np.array(labels)
		return labels

	def _read_imgs_to_numpy(self, filenames, width , height):
		imgs = []
		for filename in tqdm(filenames):
			img = read_img(filename, width , height)
			#img = normalize_img(img)
			imgs.append(img)
		imgs = np.array(imgs)
		return imgs

	def generate_imgs(self,  batch_size, augmentation = False):

		augmentator = DataAugmentator(verbose=False)

		while True:
			X = []
			Y = []
			for _ in range(batch_size) :
				img , label = next(self.zipped)
				#img_processed = augment_img(img) # (im , self.width , self.height, ordering='channels_last')

				if augmentation:
					#orig_img = img.copy()
					#orig_label = label.copy()
					p = np.random.rand(1)[0]
					if p > 0.9:
						img, label = augmentator(img, label)

				img = img.astype(np.float32)
				img = normalize_img(img, operations=[])
				
				label_processed = map_label_2_sandwich(label, self.nClasses, self.width, self.height)
				
				X.append(img)
				
				Y.append(label_processed)
			print(np.array(X).shape)
			#np.save(r"C:\Users\PR\Desktop\label_orig.npy", np.array(Y))
			yield np.array(X) , np.array(Y)


	def _reshape_image_set(self, dataset, width, height, nchannels):
		reshaped_dataset = []

		for image in dataset:
			image = image.reshape(height,width, nchannels)
			reshaped_dataset.append(image)

		return np.array(reshaped_dataset)

#TODO tested in jupyter - generally works, now we need to add option to load data from h5 in generator (overload init or sth else)
	def _read_img_from_h5_file(self, h5_filename, width , height, dataset_type, images_type = 'img'):
		'''
		Read data from h5 file to numpy arrays
		'''			
		data = h5py.File(h5_filename, 'r')
		if images_type == "labels":
			# labels_raw = data.get('/' + dataset_type +'/y')
			#Take labels from h5 file
			img_raw = data.get('/' + dataset_type +'/y')
			img = self._reshape_image_set(img_raw, width, height, 1)
		else:
			#take images
			imgs_raw = data.get('/' + dataset_type +'/x')
			img = self._reshape_image_set(imgs_raw, width, height, 3)
			

		return img
		
	
	def _get_images_list_from_h5(self, image_set):
		images = []
		for image in image_set:
			images.append(image)

		return np.array(images)



# def prepare_generators(config): 

# 	train_images_path = config['train_images_path']
# 	train_segs_path = config['train_segs_path']
# 	val_images_path = config['val_images_path']
# 	val_segs_path = config['val_segs_path']

# 	train_batch_size = config['train_batch_size']
# 	val_batch_size = config['val_batch_size']

# 	n_classes = config['n_classes']
# 	input_height = config['input_height']
# 	input_width = config['input_width']

# 	is_h5 = eval(config['read_h5'])
# 	h5_path =config['h5_file_path']
    
# 	train_dataset = DataGenerator(train_images_path, train_segs_path, input_width, input_height, n_classes, is_h5, h5_path, 'train')
# 	val_dataset = DataGenerator(val_images_path, val_segs_path, input_width, input_height, n_classes, is_h5, h5_path, 'val')

# 	train_gen  = train_dataset.generate_imgs(train_batch_size, augmentation=True)
# 	val_gen = val_dataset.generate_imgs(val_batch_size, augmentation=False)

# 	steps_per_train_epoch = np.ceil(train_dataset.dataset_size / train_batch_size)
# 	steps_per_val_epoch = np.ceil(val_dataset.dataset_size / val_batch_size)

# 	return train_gen, val_gen, steps_per_train_epoch, steps_per_val_epoch

'''[Generator adapted from image-keras-segmentation, using keras data agumentation]

:return: [description]
:rtype: [type]
'''
def prepare_generators_adapt(config_parameters, config_paths, config_classes):

	train_batch_size = config_parameters['train_batch_size']
	val_batch_size = config_parameters['val_batch_size']
	h5_path =config_paths['h5_file_path']
	height = config_parameters['input_height']
	width = config_parameters['input_width']
	classes_no = max(list(config_classes.values()))+1 # plus class 0 - background

	x_train, y_train, x_val, y_val, train_dataset_size, val_dataset_size = read_h5(h5_path)
	train_gen = data_generator(x_train, y_train, height, width, config_classes, train_batch_size, 'train') 
	val_gen = data_generator(x_val, y_val, height, width, config_classes, val_batch_size,'val')

	steps_per_train_epoch = np.ceil(train_dataset_size / train_batch_size)
	steps_per_val_epoch = np.ceil(val_dataset_size / val_batch_size)

	return train_gen, val_gen, steps_per_train_epoch, steps_per_val_epoch







# import Models , LoadBatches
# G  = LoadBatches.imageSegmentationGenerator( "data/clothes_seg/prepped/images_prepped_train/" ,  "data/clothes_seg/prepped/annotations_prepped_train/" ,  1,  10 , 800 , 550 , 400 , 272   ) 
# G2  = LoadBatches.imageSegmentationGenerator( "data/clothes_seg/prepped/images_prepped_test/" ,  "data/clothes_seg/prepped/annotations_prepped_test/" ,  1,  10 , 800 , 550 , 400 , 272   ) 

# m = Models.VGGSegnet.VGGSegnet( 10  , use_vgg_weights=True ,  optimizer='adadelta' , input_image_size=( 800 , 550 )  )
# m.fit_generator( G , 512  , nb_epoch=10 )


#### legacy reading images function
# def getImageArr( img , width , height , imgNorm="sub_mean" , ordering='channels_first' ):

# 	try:
# 		#img = cv2.imread(path, 1)

# 		if imgNorm == "sub_and_divide": 
# 			img = np.float32(cv2.resize(img, ( width , height ))) / 127.5 - 1
# 		elif imgNorm == "sub_mean":
			
# 			img = img/255.0
# 			img[:,:,0] -= 103.939/255
# 			img[:,:,1] -= 116.779/255
# 			img[:,:,2] -= 123.68/255
			
# 		elif imgNorm == "divide":
# 			img = cv2.resize(img, ( width , height ))
# 			img = img.astype(np.float32)
# 			img = img/255.0

# 		if ordering == 'channels_first':
# 			img = np.rollaxis(img, 2, 0)
# 		return img
# 	except:
# 		print('Default image with zeros - ALERT!')
# 		img = np.zeros((  height , width, 3 ))
# 		if ordering == 'channels_first':
# 			img = np.rollaxis(img, 2, 0)
# 		return img
