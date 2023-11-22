
set -e

DEVICE=$1

echo $DEVICE
su - usr_name -c '
cd /home/usr_name/Documents/yolov3-master
source /home/usr_name/anaconda3/bin/activate /home/usr_name/anaconda3/envs/yolo
rm -rf ./nohup.out
nohup python3 train.py --device '"$DEVICE"' --name voc_quant_8bit --data voc.yaml --cfg yolov3-tiny.yaml --weights runs/train/voc_full_relu/weights/best.pt --imgsz 960 &
'