
import glob
import itertools
import json
import os

import numpy as np
import pandas as pd
import PIL.Image as Image
from sklearn.metrics import (accuracy_score, auc, confusion_matrix,
                             precision_score, recall_score, roc_curve)
from tqdm import tqdm, trange

import cv2
from segmentation_module.segmentation_tools.utils2 import get_photos_from_dir


def _read_imgs_to_numpy(filenames, width=512, height=512):
    """[summary]
    
    :param filenames: [description]
    :type filenames: [type]
    :param width: [description]
    :type width: [type]
    :param height: [description]
    :type height: [type]
    :return: [description]
    :rtype: [type] 
    """

    imgs = []
    for filename in tqdm(filenames):
        img = np.asarray(Image.open(filename))
        img = cv2.resize(img, (width, height)) # TODO Do we really need to resize image here??
        if(len(img.shape) > 2):
            img = img[:,:,0]
        imgs.append(img)
    imgs = np.array(imgs)
    return imgs

def check_for_missing_class(img, n_classes):
    """[summary]
    
    :param img: [description]
    :type img: [type]
    :param n_classes: [description]
    :type n_classes: [type]
    :return: [description]
    :rtype: [type]
    """

    size_differ = n_classes - img.shape[0]
    add = np.zeros(size_differ,)
    img = np.append(img, add, axis=0)
    return img

# extract label masks from labels and predictions
def extract_masks(seg_img, cl, n_cl):
    """[summary]
    
    :param seg_img: [description]
    :type seg_img: [type]
    :param cl: [description]
    :type cl: [type]
    :param n_cl: [description]
    :type n_cl: [type]
    :return: [description]
    :rtype: [type]
    """

    h, w  = seg_img.shape[0], seg_img.shape[1]
    masks = np.zeros(( h, w, n_cl))
    
    for i, c in enumerate(cl):
        masks[ :, :, i] = seg_img == c

    return masks

def extract_classes(img):
    """Extract class count from label
    
    :param img: [description]
    :type img: [type]
    :return: [description]
    :rtype: [type]
    """

    cl = np.unique(img)
    n_cl = len(cl)

    return cl, n_cl


def extract_both_masks(eval_segm, gt_segm, cl, n_cl):
    """Extract class masks from predictions and labels
    
    :param eval_segm: [description]
    :type eval_segm: [type]
    :param gt_segm: [description]
    :type gt_segm: [type]
    :param cl: [description]
    :type cl: [type]
    :param n_cl: [description]
    :type n_cl: [type]
    :return: [description]
    :rtype: [type]
    """

    eval_mask = extract_masks(eval_segm, cl, n_cl)
    gt_mask   = extract_masks(gt_segm, cl, n_cl)

    return eval_mask, gt_mask


def check_for_missing_class2d(img, n_classes):
    """[summary]
    
    :param img: [description]
    :type img: [type]
    :param n_classes: [description]
    :type n_classes: [type]
    :return: [description]
    :rtype: [type]
    """

    width_differ = n_classes - img.shape[0]
    height_differ = n_classes - img.shape[1]
    left_pad = width_differ // 2
    right_pad = width_differ - left_pad
    up_pad = height_differ //2
    bottom_pad = height_differ - up_pad 
    img = np.pad(img,((left_pad,right_pad), (up_pad,bottom_pad)), 'constant',constant_values=(0, 0))

    return img

def convert_dict_key(classes_dict):
    classes = {}
    for key, value in classes_dict.items():
        classes[int(key)] = value
    return classes

def prepare_column_list(label_list):
    column_list =[]
    for label in label_list:
        column_list.append("Pred_" + label)
    return column_list
