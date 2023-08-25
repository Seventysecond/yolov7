# -*- coding: utf-8 -*-
'''
 Source name: detect_config.py
 Description: Loader configure file
 
 Modification history:
 Date        Ver.   Author           Comment
 ----------  -----  ---------------  -----------------------------------------
 2023/8/11  I0.00   Joey Lu           Initial Release
'''

#===============================================================================
#常更改的parameter
#===============================================================================
weights = r"runs\\train\\custom\\0802bestv0.pt"  #model.pt path(s)
source = r"D:\\yzu_learnig\\intership\\learning\\final\data\\scratched\\image" #test image path
img_size = 640  #input image size
conf_thres = 0.7  #object confidence threshold
iou_thres = 0.45  #IOU threshold for NMS
project = 'runs/detect'  #save results to project/name
name = '0811v'  #save results to project/name
#===============================================================================
#視情況更改的parameter
#===============================================================================
device = ''  #cuda device, i.e. 0 or 0,1,2,3 or cpu
view_img = False  #display results
save_txt = False  #save results to *.txt
save_conf = False  #save confidences in --save-txt labels
nosave = False  #do not save images/videos
classes = None  #filter by class: --class 0, or --class 0 2 3
agnostic_nms = False  #class-agnostic NMS
augment = False  #augmented inference
update = False  #update all models
exist_ok = False  #existing project/name ok, do not increment
no_trace = False  #don`t trace model

#===============================================================================
#parameter set end
#===============================================================================

