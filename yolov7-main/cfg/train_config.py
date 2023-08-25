# -*- coding: utf-8 -*-
'''
 Source name: train_config.py
 Description: Loader configure file
 
 Modification history:
 Date        Ver.   Author           Comment
 ----------  -----  ---------------  -----------------------------------------
 2023/8/11  I0.00   Joey Lu           Initial Release
'''
#===============================================================================
#常更改的parameter
#===============================================================================
weights = ''  #initial weights path
cfg = 'cfg/training/yolov7.yaml'  #model.yaml path
data = 'data/coco.yaml'  #data.yaml path
hyp = 'data/hyp.scratch.p5.yaml'  #hyperparameters path
epochs = 300  #traing times
batch_size = 16  #total batch size for all GPUs
img_size = [640, 640]  #[train, test] image sizes
device = '0'  #cuda device, i.e. 0 or 0,1,2,3 or cpu
workers = 8  #maximum number of dataloader workers
project = 'runs/train'  #save to project/name
name = 'yolov7'  #save to project/name
#===============================================================================
#視情況更改的parameter
#===============================================================================
rect = False  #rectangular training
resume = False  #resume most recent training
nosave = False  #only save final checkpoint
notest = False  #only test final epoch
noautoanchor = False  #disable autoanchor check
evolve = False  #evolve hyperparameters
bucket = ''  #gsutil bucket
cache_images = False  #cache images for faster training
image_weights = False  #use weighted image selection for training
multi_scale = False  #vary img-size +/- 50%%
single_cls = False  #train multi-class data as single-class
adam = False  #use torch.optim.Adam() optimizer
sync_bn = False  #use SyncBatchNorm, only available in DDP mode
local_rank = -1  #DDP parameter, do not modify
entity = None  #W&B entity
exist_ok = False  #existing project/name ok, do not increment
quad = False  #quad dataloader
linear_lr = False  #linear LR
label_smoothing = 0.0  #Label smoothing epsilon
upload_dataset = False  #Upload dataset as W&B artifact table
bbox_interval = -1  #Set bounding-box image logging interval for W&B
save_period = -1  #Log model after every "save_period" epoch
artifact_alias = 'latest'  #version of dataset artifact to be used
freeze = [0]  #Freeze layers: backbone of yolov7=50, first3=0 1 2
v5_metric = False  #assume maximum recall as 1.0 in AP calculation
#===============================================================================
#parameter set end
#===============================================================================