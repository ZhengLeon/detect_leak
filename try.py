# -- coding:UTF-8
import re
import os
import json
import cocopack
import sys

# 根据txt文件提取图片下载地址和所有图片集合对应的coco格式json文件
# 运行完成后运行get_img_file.py读取图片地址下载图片


def filetype(flines,group_len,url_posi):
	"""
	存在多重类型annotaion文件，根据文件内容判断改文件类型
	"""
	i = 0
	while(i<(len(flines)-group_len)):
		# print(i,flines[i+url_posi],flines[i+group_len-1])
		if '最终答案' == flines[i-1] and len(flines[i+url_posi])>10 and len(flines[i+group_len-1])>10:
			# print(i,flines[i+url_posi])
			if 'http' in flines[i+url_posi] and '{"result"'in flines[i+group_len-1]:
				return 0
		i = i+1
	return 1

def get_file_parm(flines):
	"""
	获取label文件特征以适应不同种类标签
	group_len一组标签所占行数
	url_posi url地址所在的相对行数

	"""
	for i in range(len(flines)):
		if flines[i] == '最终答案':
			break
	group_len = i+1
	for i in range(len(flines)):
		if flines[i] == 'url':
			break
	url_posi  = i
	for i in range(len(flines)):
		if flines[i] == 'file_name':
			break
	name_posi = i	
	return group_len,url_posi,name_posi


def generatejson():
	#base_path = '~/zly/icafe7825/'
	#raw_file_addrs= os.listdir(base_path) #得到文件夹下的所有文件名称
	raw_file_addrs = ['239372.txt',] #测试用，只分析一个文件的内容

	save_dir = './datasets.json'

	image_download_config_dir = './image_download.txt'
	image_download_urls = []

	file_type0_num = 0
	file_type1_num = 0


	BaiduData = cocopack.coco()


	for raw_file_addr in raw_file_addrs:
		print(raw_file_addr)

		if raw_file_addr[-3:] != 'txt' and  raw_file_addr[:-3] != 'TXT': 
			print(raw_file_addr,'is not a txt file....')
			continue

		raw_file = open(raw_file_addr,'r',encoding='utf-8')
		flines   = re.split('[\n\t]',raw_file.read())
		group_len,url_posi,name_posi = get_file_parm(flines)
		pic_num  = 0 #每个文件的解析图片数量

		i = 0

		if filetype(flines,group_len,url_posi) == 0:
			# print(raw_file_addr)
			file_type0_num = file_type0_num + 1
			while(i<(len(flines)-group_len+1)):
				# if len(flines[i+group_len-1])>10:
					# print(i)
				if 'http' in flines[i+url_posi] and '{"result"' in flines[i+group_len-1] \
				and 'elements":[]' not in flines[i+group_len-1]:
					image_download_url = flines[i+url_posi]
					file_name = flines[i+name_posi]
					file_val = json.loads(flines[i+group_len-1],encoding='utf-8')
					print(flines[i+url_posi],len(flines[i+url_posi]))
					process_statue = BaiduData.process_one_pic(file_name, image_download_url, file_val)
					if process_statue == True:
						image_download_urls.append(flines[i+url_posi])
						pic_num  = pic_num+1
					print(process_statue)

					i = i+group_len-1
				else:
					pass

				i = i + 1

		else:
			file_type1_num = file_type1_num + 1
			pass

		raw_file.close()

		print(group_len,url_posi,filetype(flines,group_len,url_posi),pic_num)
		#group_len 一组数据行数，url_posi图片地址的相对位置，filetype文件是否可读，pic_num文件包含的可用图片数量


	print('file_type0_num:',file_type0_num)
	print('file_type1_num:',file_type1_num)

	print('=================================================')
	# Save result
	image_download_config_file = open(image_download_config_dir,'w')
	for image_download_url in image_download_urls:
		image_download_config_file.write(image_download_url+'\n')

	image_download_config_file.close()

	print('url extract finished')

	print('json check result...')
	print('Bad image list:')
	print(BaiduData.errorlist)



	print('json package begin...')
	BaiduJson = BaiduData.json_pack()
	print('json package successfully')

	with open(save_dir, 'w') as f:
	    json.dump(BaiduJson, f)
	f.close()

	print('json  save  successfully')

	print('Repeat image:')
	print(BaiduData.repetimg)
	with open('errorlog.txt', 'w') as f:
	    f.writelines(BaiduData.repetimg)
	f.close()

	print('Image num',BaiduData.imagindex)
	print('Annotiation num',BaiduData.annoindex)

def mergeclass():
	print('merge begin')
	json_dir = './datasets.json'
	save_dir = './datasets_merged.json'
	BaiduData = cocopack.coco()

	BaiduData.json_read(json_dir)
	print('json load successfully')
	BaiduData.json_class_merge()
	BaiduJson = BaiduData.json_pack()
	print('json package successfully')

	with open(save_dir, 'w') as f:
	    json.dump(BaiduJson, f)
	f.close()

	print('json  save  successfully')



if __name__ == '__main__':
	generatejson()
	mergeclass()


















