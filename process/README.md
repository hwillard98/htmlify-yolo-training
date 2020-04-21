
Instructions:

1. Run split_data.py on vm or local machine you want to train on


2. Run Training command:

python3 train.py --data custom.data --batch 8 --accum 1 --epochs 10 --nosave --cache --weights yolov3-spp-ultralytics.pt --name custom_from_ultralytics --cfg cfg/yolov3-spp.cfg

4. Test

Test on validation set:
python3 test.py --cfg yolov3-spp.cfg --weights weights/epoch300_custom_from_ultra.pt --data data/custom.data

Test on custom data: (put data in data/samples)
python3 detect.py --weights weights/last_custom_from_scratch.pt --names data/custom.names --cfg cfg/yolov3-spp.cfg


300 epochs training data
300 epochs completed in 2.131 hours.
Epoch   gpu_mem      GIoU       obj       cls     total   targets  img_size
   299/299     6.44G      1.47      1.04     0.241      2.75        12    512: 100% 23/23 [00:24<00:00,  1.06s/it]
		Class    Images   Targets         P         R   mAP@0.5           F1: 100% 3/3 [00:01<00:00,  2.93it/s]
        all        22       155     0.678     0.649     0.623     0.654