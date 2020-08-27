import json

def countX(lst, x):
    return lst.count(x)

with open("datasets_merged.json","r") as load_f:
    load_dict=json.load(load_f)
    itemlist=[key for key in load_dict['annotations']]

result = {}
image_anno=[]
image_id = []
image_name= []
for i,item in enumerate(itemlist):
    image_id.append(item['image_id'])
for i in range(len(set(image_id))):
    image_anno.append([])
    image_name.append([])

for i,item in enumerate(itemlist):
    item_anno = item['bbox']+[item['category_id']]
    image_anno[item['image_id']].append(item_anno)
    image_name[item['image_id']].append(load_dict['images'][item['image_id']]['file_name'])

for i in range(len(image_anno)):
    result[image_name[i][0]]=image_anno[i]


with open('aicv.image.boxes', 'w') as outfile:
    json.dump(result, outfile)
