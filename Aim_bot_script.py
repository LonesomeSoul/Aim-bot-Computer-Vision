#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2,keyboard,pyautogui as pg, numpy as np,os,gc,sys,math
#import pydirectinput as pdi
from time import sleep
from win32api import GetSystemMetrics
#import utils
#import torch
from torch.hub import load
import random
import win32gui, win32ui, win32con, win32api


# In[ ]:





# In[4]:


def dots_distance(p1,p2):
    return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

def nothing(args):pass

def move_mouse_to_target(targets_arr,center_x,center_y):
    global screen_size_x,screen_size_y,abs_multi_x,abs_multi_y,screen_region
    target_xy=[0,0]
    target_idx=0
    if (targets_arr.shape[0]==0):
        return 0
    if (targets_arr.shape[0]>0):
        min_dist=screen_size_x+screen_size_y
        for i in range(targets_arr.shape[0]):
            this_box_center_x=(targets_arr[i][0]+targets_arr[i][2])//2+screen_region[0]
            this_box_center_y=(targets_arr[i][1]+targets_arr[i][3])//2+screen_region[1]
            this_dist=dots_distance([center_x,center_y],[this_box_center_x,this_box_center_y])
            if (this_dist<min_dist):
                min_dist=this_dist
                target_idx=i
                target_xy=[this_box_center_x,this_box_center_y]
    cursor_iterations=1
    sum_dist_x=(target_xy[0]-center_x)/10
    sum_dist_y=(target_xy[1]-center_y)/16
    add_x=int(round(sum_dist_x-int(sum_dist_x), 2)*abs_multi_x)
    add_y=int(round(sum_dist_y-int(sum_dist_y), 2)*abs_multi_y)
    sum_dist_x=int(sum_dist_x)
    sum_dist_y=int(sum_dist_y)
    if (cursor_iterations>1):
        dist_iter_x=int(sum_dist_x/cursor_iterations)
        dist_iter_y=int(sum_dist_y/cursor_iterations)
    else:
        dist_iter_x=sum_dist_x
        dist_iter_y=sum_dist_y
    for i in range(cursor_iterations):
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,dist_iter_x*abs_multi_x+add_x, dist_iter_y*abs_multi_y+add_y, 0, 0)
        #sleep(random.uniform(0.001, 0.002))
    #pg.moveTo(center_x,center_y)
    #pg.moveRel(sum_dist_x,sum_dist_y,duration=0)


# In[ ]:





# In[ ]:


model = load('ultralytics/yolov5', 'custom', path=r'yolov5_weights.pt', force_reload=True)


# In[5]:


cv2.waitKey(2000)
#screen_count=len(os.listdir(root_path))
img_np=np.array(pg.screenshot())
post_process=0
model_active=0
model.conf=0.25
window_size_x=1000
window_size_y=1000
screen_size_x=GetSystemMetrics(0)
screen_size_y=GetSystemMetrics(1)
abs_multi_x=65535//screen_size_x
abs_multi_y=65535//screen_size_y+1
center_x=int(screen_size_x/2)
center_y=int(screen_size_y/2)
screen_region=[center_x-window_size_x//2, center_y-window_size_y//2, window_size_x, window_size_y]
wait_time=1000
aim_bot_active=0
while True:
    img_np=np.array(pg.screenshot(region=(screen_region)))
    frame = img_np[:,:,::-1]
    if (model_active):
        results=model(frame)
        frame=np.array(results.render()[0])
        wait_time=10
    #cv2.imshow('frame', frame)
    #if (keyboard.is_pressed("n") and model_active==1):
    cv2.waitKey(wait_time)
    if (keyboard.is_pressed("n") and aim_bot_active==0):
        aim_bot_active=1
        model_active=1
    if (keyboard.is_pressed("n") and aim_bot_active==1):
        aim_bot_active=0
        model_active=0
    if (aim_bot_active):
        move_mouse_to_target(results.xyxy[0].cpu().numpy(),center_x,center_y)
    if keyboard.is_pressed("v"):
        sleep(5)
    #if keyboard.is_pressed("escape") or keyboard.is_pressed("x"):
    if keyboard.is_pressed("x"):
        break
#cv2.destroyWindow("frame")


# In[ ]:





# In[ ]:





# In[ ]:




