import os
import cocopack
# import urllib.request

json_dir = './datasets.json'

save_dir = './predictimages/'

if not os.path.exists(save_dir):
    os.system('sudo mkdir '+save_dir)
#    os.system('work@qm')

BaiduData = cocopack.coco()
BaiduData.json_read(json_dir)
print('Load json succefully')

image_download_names = []
image_download_urls  = []
error_list           = []

for i in range(len(BaiduData.localdata_imag)):
	image_download_names.append(BaiduData.localdata_imag[i]['file_name'])
	image_download_urls. append(BaiduData.localdata_imag[i]['coco_url'])

for i in range(len(image_download_urls)):
	image_download_name = image_download_names[i]
	image_download_url  = image_download_urls[i]

	if 'http' in image_download_url:
		if os.path.exists(save_dir+image_download_name):
			print(image_download_name+'exist')
		else:
			# cmd = 'sudo wget --no-check-certificate '+image_download_url+' -O '+save_dir+image_download_name
			cmd = 'wget -c --header="Referer: http://test.baidu.com/" --no-check-certificate '+image_download_url+' -O '+save_dir+image_download_name
			os.system(cmd)
	else:
		error_list.append(image_download_url)

print('Download Finished')


print('Error list')
print(error_list)


