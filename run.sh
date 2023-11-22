sleep 5
source activate monitor
cd /path/to/nvidia-smi-helper
rm -rf ./nohup.out
nohup python app.py &
