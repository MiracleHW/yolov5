import cv2
import os
import glob
import random
import numpy as np

class AddBackground():
    def __init__(self,background_dir,min_ratio=0.4,max_ratio=0.8):
        if not os.path.exists(background_dir):
            raise ValueError("background dir not exists")

        self.background_list=glob.glob(os.path.join(background_dir,"*.jpg"))
        self.min_ratio=min_ratio
        self.max_ratio=max_ratio

    def __call__(self,img,labels):

        bg_path=random.choice(self.background_list)
        bg=cv2.imread(bg_path)

        bgh,bgw=bg.shape[:2]
        imh,imw=img.shape[:2]

        imbg_ratio=min(bgh/imh,bgw/imw)
        min_ratio=self.min_ratio*imbg_ratio
        max_ratio=self.max_ratio*imbg_ratio

        resize_ratio=random.uniform(min_ratio,max_ratio)
        resize_img=cv2.resize(img,dsize=None,fx=resize_ratio,fy=resize_ratio)

        labels[:,1:5]=labels[:,1:5]*resize_ratio
        reh,rew=resize_img.shape[:2]

        x1=random.uniform(bgw*self.min_ratio,bgw*self.max_ratio-rew)
        y1=random.uniform(bgh*self.min_ratio,bgh*self.max_ratio-reh)
        x1,y1=int(x1),int(y1)

        bg[y1:y1+reh,x1:x1+rew]=resize_img
        labels[:,1]+=x1
        labels[:,2]+=y1
        labels[:,3]+=x1
        labels[:,4]+=y1

        return bg,labels



if __name__=="__main__":
    m=AddBackground("../mydata/bg")

    img=cv2.imread("../mydata/0001.jpg")

    for i in range(10):
        bg,_=m(img,np.array([50,50,300,300]))
        cv2.imshow("im",bg)
        cv2.waitKey(0)