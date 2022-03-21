import cv2
import glob
import os
import shutil
import uuid

data_images="images"
data_labels="labels"

data_out="object_image"
classes=open(os.path.join(data_labels,"classes.txt")).read().split("\n")
if(classes[-1]==""):
    classes=classes[:-1]
if(os.path.isdir(data_out)):
    shutil.rmtree(data_out)
os.mkdir(data_out)
for cl in classes:
    os.mkdir(os.path.join(data_out,cl))

def anno2xywh(line,h,w):
    id_,x_center,y_center,width_,height_=line.split(" ")
    return classes[int(id_)],int(float(x_center)*w),int(float(y_center)*h),int(float(width_)*w),int(float(height_)*h)

for img_path in tqdm.tqdm(glob.glob(os.path.join(data_images,"*"))):

    image= cv2.imread(img_path)
    txt_path =(img_path[:-len(img_path.split(".")[-1])]+"txt").replace(data_images,data_labels)
    h,w=image.shape[:2] 
    if(not os.path.isfile(txt_path)) : continue
    f=open(txt_path,"r")
    for line in f.read().split("\n"):
        if(line==""): continue
        lb,x_center,y_center,width,height = anno2xywh(line,h,w)
        x1=x_center-width//2
        y1=y_center-height//2
        x2=x_center+width//2
        y2=y_center+height//2
        img_crop = image[y1:y2,x1:x2]
        cv2.imwrite(os.path.join(data_out,lb,str(uuid.uuid4())+".jpg"),img_crop)
        

