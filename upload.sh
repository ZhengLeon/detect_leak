BOS_AK="43c2fb7564a74f8eb25129abcb227426" 
BOS_SK="d3411bab6a4c44a08fd0fac8ce478a2f"
BOS_URL="bj.bcebos.com"
#BOS_MODELFOLDER= "v1/zhongce-yy"

# 根据当前时间戳和 uuid 生成唯一文件名，上传至 bos
current_timestamp=`date +%s%3N`
uuid=`cat /proc/sys/kernel/random/uuid`
file_type='.tar.bz2'
bos_file_name=$current_timestamp$uuid$file_type
echo $bos_file_name
upload_ret=`python3 ~/zly/detectron2_repo/upload_file.py $BOS_AK $BOS_SK $BOS_URL v1/zhongce-yy ~/zly/icafe7825/leakimages.tar.bz2 $bos_file_name`
