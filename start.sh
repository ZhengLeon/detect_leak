function cleanTempFile(){
    rm -f ~/zly/icafe7825/input.txt
    rm -f ~/zly/icafe7825/errorlog.txt
    rm -f ~/zly/icafe7825/image_download.txt
    rm -rf ~/zly/icafe7825/predictimages
    mkdir ~/zly/icafe7825/predictimages
    rm -f ~/zly/icafe7825/aicv.image.boxes
    rm -f ~/zly/icafe7825/datasets.json
    rm -f ~/zly/icafe7825/datasets_merged.json
    rm -f ~/zly/icafe7825/detectron.result.leak
    echo "temp file cleaned"
}
cleanTempFile

# 通过接口下载待测试文件
#wget $BOS_TXT_FILE -O ~/zly/icafe7825/input.txt

# 转化数据标签
python3 ~/zly/icafe7825/try.py 
python3 ~/zly/icafe7825/merged_json2txt.py

# 下载图片
python3 ~/zly/icafe7825/get_img_file.py

# 调用模型进行预测
python3 ~/zly/detectron2_repo/demo/predict_icafe7825.py --config-file ~/zly/detectron2_repo/configs/COCO-Detection/my_faster_rcnn_X_101_32x8d_FPN_3x.yaml --input ~/zly/icafe7825/predictimages --aicv-data ~/zly/icafe7825/aicv.image.boxes --detectresult-out ~/zly/icafe7825/detectron.result --opts MODEL.WEIGHTS  ~/zly/detectron2_repo/output/model_final.pth

# 将漏标的图画出来
python3 plot_leak.py

# 将结果~/zly/icafe7825/detectron.result.leak上传
