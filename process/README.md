
Instructions:

1. Run split_data.py on vm or local machine you want to train on

2. Copy test.txt train.txt dev.txt custom.data and custom.names into yolov3/data folder

3. Run Training command:

python3 train.py --data custom.data --batch 8 --accum 1 --epochs 10 --nosave --cache --weights yolov3-spp-ultralytics.pt --name custom_from_ultralytics --cfg cfg/yolov3-spp.cfg

4. Test: (copy test file to data/samples/)

python3 detect.py --weights weights/last_custom_from_scratch.pt --names data/custom.names --cfg cfg/yolov3-spp.cfg