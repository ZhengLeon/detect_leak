import json
import os
import cv2

save_dir= 'leakimages/'
if not os.path.exists(save_dir):
    os.system('mkdir '+save_dir)

with open("detectron.result.leak","r") as load_f:
    load_dict=json.load(load_f)
    itemlist=[key for key in load_dict]
for item in  itemlist:
    image_path = './predictimages/'+item
    img = cv2.imread(image_path) 
    for box in load_dict[item]:
        img = cv2.rectangle(img, (box[0],box[1]), (box[0]+box[2],box[1]+box[3]), (0,0,255), 2)
    cv2.imwrite(save_dir+item+'.jpg',img)
