import requests
import json
import glob
import random
import shutil
import os
from PIL import Image, ImageEnhance

from os import path

print("Starting data download")

DATA_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'export-2020-04-16T16_57_05.518Z.json')
DATASET = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dataset')

with open(DATA_FILE, 'r') as f:
	labeldict = json.load(f)


# download dataset
for item in labeldict:
	filename = os.path.join(DATASET, item['ID'] + '.jpg')	
	if not path.exists(filename):
		img_data = requests.get(item['Labeled Data']).content
		with open(filename, 'wb') as handler:
			handler.write(img_data)

print("Dataset download complete")

data_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")), "data")

BASE = os.path.join(data_path, "images")
TRAIN = os.path.join(BASE, "train")
DEV = os.path.join(BASE, "validation")
TEST = os.path.join(BASE, "test")
BASE_LABELS = os.path.join(data_path, "labels")
TRAIN_LABELS = os.path.join(BASE_LABELS, "train")
DEV_LABELS = os.path.join(BASE_LABELS, "validation")
TEST_LABELS = os.path.join(BASE_LABELS, "test")

# Clean up old files from previous script runs
# and create file structure
for directory in [BASE, BASE_LABELS, TRAIN, DEV, TEST, TRAIN_LABELS, DEV_LABELS, TEST_LABELS]:
	if os.path.exists(directory):
		shutil.rmtree(directory, ignore_errors=False,
								onerror=None)
	os.mkdir(directory)


# Get dataset
dataset = glob.glob(os.path.join(DATASET, '*.jpg'))

print("Preprocessing images")

#preprocessing
for file in dataset:
	image = Image.open(file).convert('L')
	enhancer = ImageEnhance.Contrast(image)
	enhanced_im = enhancer.enhance(1.0)
	enhanced_im.save(file)


# Combines files into one list
size = len(dataset)
ratio_dev = 0.1
ratio_test = 0
num_dev = int(size * ratio_dev)
num_test = int(size * ratio_test)
num_train = size - num_dev - num_test
print("Number of files: ", size, " split ", num_train, "|", num_dev, "|", num_test)

def get_class(title):
	if title == "heading":
		return 0
	if title == "paragraph":
		return 1
	if title == "image":
		return 2
	if title == "listelement":
		return 3
	if title == "button":
		return 4
	if title == "list":
		return 5


def create_label_file(image_dir, label_dir, label, filename):
	# One row per object
	# Each row is class x_center y_center width height format.
	# Box coordinates must be in normalized xywh format (from 0 - 1). 
	# If your boxes are in pixels, divide x_center and width by image width, and y_center and height by image height.
	# Class numbers are zero-indexed (start from 0).
	image = Image.open(image_dir + '/' + filename)
	img_width, img_height = image.size

	f = open(label_dir + '/' + filename.split('.')[0] + '.txt', 'w')
	objects = label["Label"]["objects"]
	for item in objects:
		item_class = get_class(item["title"])
		top = item["bbox"]["top"]
		left = item["bbox"]["left"]
		height = item["bbox"]["height"]
		width = item["bbox"]["width"]

		x_center = left + width/2
		y_center = top + height/2

		x_center /= img_width
		width /= img_width
		y_center /= img_height
		height /= img_height
		f.write(str(item_class) + ' ' + str(x_center) + ' ' + str(y_center) + ' ' + str(width) + ' ' + str(height) + '\n')
	f.close()

# Move files to appropriate set
def create_set(text_file, num, IMAGES, LABELS):
	data_file = open(os.path.join(data_path, text_file), 'w')
	for _ in range(num):
		file_num = random.randint(0, len(dataset)-1)
		filename = os.path.basename(dataset[file_num])
		shutil.copy2(dataset[file_num], IMAGES)
		del dataset[file_num]
		label = next(item for item in labeldict if item["ID"] == filename.split('.')[0])
		create_label_file(IMAGES, LABELS, label, filename)
		data_file.write(os.path.join(IMAGES, filename) + '\n')
	data_file.close()

if num_test > 0:
	create_set("test.txt", num_test, TEST, TEST_LABELS)
create_set("dev.txt", num_dev, DEV, DEV_LABELS)
create_set("train.txt", num_train, TRAIN, TRAIN_LABELS)

print("Train/val/test split complete")




