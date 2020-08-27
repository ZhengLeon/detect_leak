# -- coding:UTF-8
import json
import re
import os
import sys


class coco:

	def __init__(self):
		# reload(sys)
		# sys.setdefaultencoding('utf8') 

		#############################
		# info
		description='Baidu internal test'
		url=''
		version='0.1'
		year='2020'
		contributor='Annonymous'
		date_created='2020/06/23'
		self.localdata_info = {u'description':description, 
							   u'url':url, 
							   u'version':version, 
							   u'year':year, 
							   u'contributor':contributor, 
							   u'date_created':date_created}

		#############################
		# licenses
		license_1 = {u'description':'None', 
					 u'url':'', 
			 		 u'id':1}
		self.localdata_lice = [license_1,]

		#############################
		# categories

		self.cclasses = {'2座微型车':1,'两厢车':2,'三厢车':3,'跑车':4,'小型suv':5,'中大型suv':6,
						 '皮卡':7,'小货车':8,'大货车':10,'微面':11,'商务车':12,'轻型客车':13,
						 '小型巴士':14,'单层大巴车':15,'双层大巴车':16,'多节大巴车':17,'行人-站立':18,
						 '行人-坐姿':19,'行人-蹲姿/弯腰':20,'儿童-站立':21,'儿童-坐姿':22,'儿童-蹲姿/弯腰':23,
						 '自行车':24,'大型机动三轮车':25,'厢式三轮车':26,'普通人力/助力三轮车':27,'摩托车/电动车':28,
						 '手推车':29,'交通锥桶':30,'交通桩':31,'水马':32,'防撞桶':33,'水泥隔离墩':34,'石墩':35,'停车指示牌':36,
						 '临时交通标示':37,'三角警示牌':38}

		self.localdata_cate = []

		for classname in self.cclasses.keys():
			self.localdata_cate.append({u'supercategory': u'None', 
										u'id': self.cclasses[classname],
										u'name': classname})


		self.localdata_imag = []
		self.localdata_anno = []
		self.errorlist      = []
		self.iiddict        = {}
		self.repetimg       = []
		self.imagindex      = 0
		self.annoindex      = 0
		self.classstatic    = {}#统计各类别数量
		for classname in self.cclasses.keys():
			self.classstatic[classname] = 0

		# self.encodetype = sys.getfilesystemencoding()

		# {u'license': 4, u'file_name': u'000000397133.jpg', u'coco_url': u'http://images.cocodataset.org/val2017/000000397133.jpg', 
		#  u'height': 427, u'width': 640, u'date_captured': u'2013-11-14 17:02:52', 
		#  u'flickr_url': u'http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg', 
		#  u'id': 397133}
		# for i in range(1):
		# 	localdata_imag.append({u'license':1, u'file_name':'', u'coco_url':'',
		# 						   u'height':000, u'width':000, 
		# 						   u'date_captured':'2013-11-14 17:02:52', 
		# 						   u'flickr_url':'', u'id':000001})
		# pass


	def insert_image(self,file_name,coco_url,height,width,date,flickr_url,image_id,license=1):
		self.localdata_imag.append({u'license':license, u'file_name':file_name, u'coco_url':coco_url,
								   	u'height':height, u'width':width, 
									u'date_captured':date, 
									u'flickr_url':flickr_url, u'id':image_id})
		self.imagindex = self.imagindex+1
		pass


	def insert_annotation(self,image_id,bbox,category_id,annotation_id,segmentation=[[]],area=0,iscrowd=0):
		self.localdata_anno.append({u'segmentation':segmentation, u'area':area, u'iscrowd':iscrowd, 
									u'image_id':image_id, 
									u'bbox':bbox, 
									u'category_id':category_id,     u'id':annotation_id})
		self.annoindex = self.annoindex+1
		pass


	def process_one_pic(self,file_name,image_download_url,file_val):
		iid          = self.imagindex
		filename    = image_download_url.split('/')[-1][:-4]
		coco_url     = image_download_url
		bboxs        = []
		category_ids = []
		date         = ''
		# print(image_download_url)
		file_val['result'][0]['size']['width']
		len(file_val['result'][0]['elements'])
		file_val['result'][0]['elements'][0]['markType']
		file_val['result'][0]['elements'][0]['text']
		int(file_val['result'][0]['elements'][0]['posX'])

		try:
			width    = file_val['result'][0]['size']['width']
			height   = file_val['result'][0]['size']['height']
			for i in range(len(file_val['result'][0]['elements'])):
				if file_val['result'][0]['elements'][i]['markType'] == 'rect':
					#print(file_val['result'][0]['elements'][i]['text'])
					if self.cclasses.__contains__(file_val['result'][0]['elements'][i]['text'].split('_')[1] ) == True:
						# print('OK 1')
						category_ids.append(self.cclasses[file_val['result'][0]['elements'][i]['text'].split('_')[1] ])
						bboxs.append([int(file_val['result'][0]['elements'][i]['posX']),
									 int(file_val['result'][0]['elements'][i]['posY']),
									 int(file_val['result'][0]['elements'][i]['width']),
									 int(file_val['result'][0]['elements'][i]['height'])])
						self.classstatic[file_val['result'][0]['elements'][i]['text'].split('_')[1] ] += 1

					elif self.cclasses.__contains__(file_val['result'][0]['elements'][i]['text'].split('_')[0] ) == True:
						# print('OK 0')
						category_ids.append(self.cclasses[file_val['result'][0]['elements'][i]['text'].split('_')[0] ])
						bboxs.append([int(file_val['result'][0]['elements'][i]['posX']),
									  int(file_val['result'][0]['elements'][i]['posY']),
									  int(file_val['result'][0]['elements'][i]['width']),
									  int(file_val['result'][0]['elements'][i]['height'])])
						self.classstatic[file_val['result'][0]['elements'][i]['text'].split('_')[0] ] += 1
					else:
						# print(self.encodetype)
						# print(self.classstatic.keys())
						#print(file_val['result'][0]['elements'][i]['text'].split('_')[0] ,file_val['result'][0]['elements'][i]['text'].split('_')[1] )
						print('Unknow class')

		except KeyError:
			print('KeyError')
			self.errorlist.append(image_download_url)
			return False

		if len(category_ids)==0:
			print('No category_ids')
			self.errorlist.append(image_download_url)
			return False

		for i in range(len(category_ids)):
			self.insert_annotation(iid,bboxs[i],category_ids[i],self.annoindex)

		self.insert_image(filename,coco_url,height,width,date,coco_url,iid,license=1)

		return True



	def json_pack(self):
		datasets = {u'info'      :self.localdata_info,   u'licenses':self.localdata_lice,
					u'images'    :self.localdata_imag,   u'annotations':self.localdata_anno,
					u'categories':self.localdata_cate,
					u'classstatic':self.classstatic
					}
		return datasets


	def json_read(self,json_dir):
		val = json.load(open(json_dir, 'r'))
		self.localdata_info = val['info']
		self.localdata_lice = val['licenses']
		self.localdata_imag = val['images']
		self.localdata_anno = val['annotations']
		self.localdata_cate = val['categories']

		if val.__contains__('classstatic'):
			self.classstatic    = val['classstatic']
		else:
			self.classstatic    = {}#统计各类别数量

			classid2class = {}
			self.cclasses = []
			for i in range(len(self.selflocaldata_cate)):
				classid2class[self.localdata_cate[i]['id']] = self.localdata_cate[i]['name']
				# self.cclasses[self.localdata_cate[i]['name']] = self.localdata_cate[i]['id']
				self.cclasses.append(self.localdata_cate[i]['name'])

			for classname in self.cclasses.keys():
				self.classstatic[classname] = 0

			for i in range(len(self.localdata_anno)):
				self.classstatic[classid2class[self.localdata_anno[i]['image_id']] ] += 1

	def json_image_del(self,image_dir):
		"""
		根据已下载的图片删除json多余的标签
		"""
		# image_save_dir = image_dir
		raw_file_addrs = os.listdir(image_dir)
		img_ids = []
		img_ids_dict = {}


		for raw_file_addr in raw_file_addrs:
			
			if raw_file_addr[-3:] != 'jpg' and  raw_file_addr[:-3] != 'JPG':
				print(raw_file_addr,'is not a image')
				continue

			img_name = raw_file_addr.split('/')[-1]
			img_id   = int(''.join(re.findall('\d+', img_name)))
			img_ids.append(img_id)
			img_ids_dict[img_id] = 1
		
		print(len(img_ids))
		print('id:',img_ids[0])

		#可用tqdm进行可视化
		logs = []
		for i in range(len(self.localdata_imag)-1,-1,-1):
			# if self.localdata_imag[i]['id'] not in img_ids:
			# 	del self.localdata_imag[i]
			try:
				if img_ids_dict[self.localdata_imag[i]['id']] == 1:
					pass
				else:
					del self.localdata_imag[i]
			except KeyError:
				del self.localdata_imag[i]
			else:
				pass

			log = 100-int(i/len(self.localdata_imag)*100)
			if  log%5 == 0 and log not in logs:
				print('process image',log,'%')
				logs.append(log)
				# break

		logs = []
		for i in range(len(self.localdata_anno)-1,-1,-1):
			# if self.localdata_anno[i]['image_id'] not in img_ids:
			# 	del self.localdata_anno[i]
			try:
				if img_ids_dict[self.localdata_anno[i]['image_id']] == 1:
					pass
				else:
					del self.localdata_anno[i]
			except KeyError:
				del self.localdata_anno[i]
			else:
				pass

			log = 100-int(i/len(self.localdata_anno)*100)
			if  log%5 == 0 and log not in logs:
				print('process annotations',log,'%')
				logs.append(log)


	def json_class_merge(self):
		convertmap = {'2座微型车':'小汽车','两厢车':'小汽车','三厢车':'小汽车','跑车':'小汽车','小型suv':'小汽车','中大型suv':'小汽车',
					  '皮卡':'小汽车','小货车':'卡车/货车','大货车':'卡车/货车','微面':'面包车','商务车':'面包车','轻型客车':'面包车',
					  '小型巴士':'大客车','单层大巴车':'大客车','双层大巴车':'大客车','多节大巴车':'大客车','行人-站立':'行人',
					  '行人-坐姿':'行人','行人-蹲姿/弯腰':'行人','儿童-站立':'行人','儿童-坐姿':'行人','儿童-蹲姿/弯腰':'行人',
					  '自行车':'自行车','大型机动三轮车':'三轮车','厢式三轮车':'三轮车','普通人力/助力三轮车':'三轮车','摩托车/电动车':'摩托车/电动车',
					  '手推车':'手推车','交通锥桶':'交通锥桶','交通桩':'交通桩','水马':'交通桩','防撞桶':'防撞桶','水泥隔离墩':'水泥隔离墩','石墩':'石墩','停车指示牌':'标示',
					  '临时交通标示':'标示','三角警示牌':'标示'}
		classnames =list(set([convertmap[i] for i in convertmap.keys()]))
		# print('classnames:',classnames)
		cclasses_new = {}
		for i in range(len(classnames)):
			cclasses_new[classnames[i]] = i

		oldclassid2new ={}
		for i in range(len(self.localdata_cate)):
			# if cclasses_new.__contains__(self.localdata_cate[i]['name'])
			oldclassid2new[self.localdata_cate[i]['id']] = cclasses_new[convertmap[self.localdata_cate[i]['name']]]

		for i in range(len(self.localdata_anno)-1,-1,-1):
			self.localdata_anno[i]['category_id'] = oldclassid2new[self.localdata_anno[i]['category_id']]


		# for i in range(len(self.localdata_cate)-1,-1,-1):
		# 	self.localdata_cate[i]['id']   = oldclassid2new[self.localdata_cate[i]['id']]
		# 	self.localdata_cate[i]['name'] = convertmap[self.localdata_cate[i]['name']]
		self.localdata_cate = []
		for classname in cclasses_new.keys():
			self.localdata_cate.append({u'supercategory': u'None', 
										u'id': cclasses_new[classname],
										u'name': classname})		


		
		self.cclasses       = []
		self.classstatic    = {}#统计各类别数量
		classid2class = {}
		for i in range(len(self.localdata_cate)):
			classid2class[self.localdata_cate[i]['id']] = self.localdata_cate[i]['name']
			# self.cclasses[self.localdata_cate[i]['name']] = self.localdata_cate[i]['id']
			self.cclasses.append(self.localdata_cate[i]['name'])
		for classname in self.cclasses:
			self.classstatic[classname] = 0
		for i in range(len(self.localdata_anno)):
			self.classstatic[classid2class[self.localdata_anno[i]['category_id']]] += 1
		# print (cclasses_new)
		# print (oldclassid2new)
		#print (self.localdata_cate)
		#print (self.classstatic)

		























