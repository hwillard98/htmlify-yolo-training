
Instructions:

1. Run split_data.py on vm or local machine you want to train on


2. Run Training command:

python3 train.py --data custom.data --batch 8 --accum 1 --epochs 10 --nosave --cache --weights yolov3-spp-ultralytics.pt --name custom_from_ultralytics --cfg cfg/yolov3-spp.cfg

4. Test

Test on validation set:
python3 test.py --cfg yolov3-spp.cfg --weights weights/epoch300_custom_from_ultra.pt --data data/custom.data

Test on custom data: (put data in data/samples)
python3 detect.py --weights weights/last_custom_from_scratch.pt --names data/custom.names --cfg cfg/yolov3-spp.cfg --source data/images/validation


original data
300 epochs completed in 2.131 hours.
Class    Images   Targets      P         R   	mAP@0.5   F1: 100% 3/3 [00:01<00:00,  2.93it/s]
all        22       155     0.678     0.649     0.623     0.654


original pre-processed data
300 epochs completed in 1.323 hours.
Class    Images   Targets     P         R   mAP@0.5   	  F1: 100% 2/2 [00:03<00:00,  1.93s/it]
all        22       148     0.822     0.897     0.917     0.853


method 2 pre-processed data
Class    Images   Targets         P         R   mAP@0.5        F1: 100% 3/3 [00:01<00:00,  1.63it/s]
all        22       175     0.805     0.876     0.884     0.836


original pre-processed data fixed dataset