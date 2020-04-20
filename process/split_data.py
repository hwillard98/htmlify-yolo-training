import requests
import json
import glob
import random
import shutil
import os
from PIL import Image, ImageEnhance

from os import path

# "datasets": [
# 	{
# 	"name": "HTML Images Howie",
# 	"id": "ck8opvcvmivle0886lxn0t33r"
# 	},
# 	{
# 	"name": "HTML Images Sunny",
# 	"id": "ck8p5sc4ktrz907289vamdq1e"
# 	},
# 	{
# 	"name": "HTML Images Jimmy",
# 	"id": "ck8p67p6tcm930902ka2s0j6p"
# 	},
# 	{
# 	"name": "HTML Images Searle",
# 	"id": "ck8q29e4dzeq40902y23oanqr"
# 	},
# 	{
# 	"name": "HTML Images Shui",
# 	"id": "ck8qgvm3kl4vf0886oryyo3ta"
# 	}
# dataset_howie = client.get_dataset("ck8opvcvmivle0886lxn0t33r")
# dataset_sunny = client.get_dataset("ck8p5sc4ktrz907289vamdq1e")
# dataset_jimmy = client.get_dataset("ck8p67p6tcm930902ka2s0j6p")
# dataset_tommy = client.get_dataset("ck8q29e4dzeq40902y23oanqr")
# dataset_shui = client.get_dataset("ck8qgvm3kl4vf0886oryyo3ta")
#API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjazhvcHNieHRxMXB6MDcxNmhvdXNmZ29mIiwib3JnYW5pemF0aW9uSWQiOiJjazhvcHNieGFpdHdoMDg4NjVmMTE2dGU4IiwiYXBpS2V5SWQiOiJjazkzMGt3ZTFrazVtMDk0MHFleGtld2tyIiwiaWF0IjoxNTg3MDU2Njk2LCJleHAiOjIyMTgyMDg2OTZ9.gl5KqwIXa1OHAGsXf9wnqy5NeBERxrj7m1TPD4FmWPU'
#client = Client()

print("Starting data download")

DATA_FILE = os.path.join(os.getcwd(), 'export-2020-04-16T16_57_05.518Z.json')

with open(DATA_FILE, 'r') as f:
	labeldict = json.load(f)

# download dataset
for item in labeldict:
	filename = 'dataset/' + item['ID'] + '.jpg'	
	if not path.exists(filename):
		img_data = requests.get(item['Labeled Data']).content
		with open(filename, 'wb') as handler:
			handler.write(img_data)

print("Dataset download complete")

BASE = os.path.join(os.getcwd(), "images")
TRAIN = os.path.join(os.getcwd(), "images/train")
DEV = os.path.join(os.getcwd(), "images/validation")
TEST = os.path.join(os.getcwd(), "images/test")
BASE_LABELS = os.path.join(os.getcwd(), "labels")
TRAIN_LABELS = os.path.join(os.getcwd(), "labels/train")
DEV_LABELS = os.path.join(os.getcwd(), "labels/validation")
TEST_LABELS = os.path.join(os.getcwd(), "labels/test")

# Clean up old files from previous script runs
# and create file structure
for directory in [BASE, BASE_LABELS, TRAIN, DEV, TEST, TRAIN_LABELS, DEV_LABELS, TEST_LABELS]:
	if os.path.exists(directory):
		shutil.rmtree(directory, ignore_errors=False,
								onerror=None)
	os.mkdir(directory)


# Get dataset
dataset = glob.glob('dataset/*.jpg')


#preprocessing
for file in dataset:
	print(file)
	image = Image.open(file).convert('L')
	enhancer = ImageEnhance.Contrast(image)
	enhanced_im = enhancer.enhance(1.0)
	enhanced_im.save(file)



# Combines files into one list
size = len(dataset)
ratio_dev = 0.1
ratio_test = 0.1
num_dev = int(size * ratio_dev)
num_test = int(size * ratio_test)
print("Number of files: ", size)

# TODO seperate JSON by set


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


# Move files to dev set
dev_data = open("dev.txt", 'w')
for _ in range(num_dev):
	file_num = random.randint(0, len(dataset)-1)
	filename = os.path.basename(dataset[file_num])
	shutil.copy2(dataset[file_num], DEV)
	del dataset[file_num]
	print("File ", filename, " moved to validation set")
	label = next(item for item in labeldict if item["ID"] == filename.split('.')[0])
	create_label_file(DEV, DEV_LABELS, label, filename)
	dev_data.write(os.path.abspath(DEV) + '/' + filename + '\n')
dev_data.close()

# move files to test
test_data = open("test.txt", 'w')
for _ in range(num_test):
	file_num = random.randint(0, len(dataset)-1)
	filename = os.path.basename(dataset[file_num])
	shutil.copy2(dataset[file_num], TEST)
	del dataset[file_num]
	print("File ", filename, " moved to test set")
	label = next(item for item in labeldict if item["ID"] == filename.split('.')[0])
	create_label_file(TEST, TEST_LABELS, label, filename)
	test_data.write(os.path.abspath(TEST) + '/' + filename + '\n')
test_data.close()

# with open('test.json', 'w') as outfile:
#     json.dump(test_json, outfile)

# # Move remaining files to train
train_data = open("train.txt", 'w')
for file in dataset:
	filename = os.path.basename(file)
	shutil.copy2(file, TRAIN)
	print("File ", filename, " moved to train set")
	label = next(item for item in labeldict if item["ID"] == filename.split('.')[0])
	create_label_file(TRAIN, TRAIN_LABELS, label, filename)
	train_data.write(os.path.abspath(TRAIN) + '/' + filename + '\n')
train_data.close()


print("Train/val/test split complete")





