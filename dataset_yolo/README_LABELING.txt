DATASET YOLO OBJECT DETECTION - 200 IMAGES

Classes:
0 = balok_hijautua
1 = balok_hitam
2 = balok_merahmuda
3 = papan_balok

Total:
- 200 images
- 200 YOLO label files
- 50 images per class
- one target object per image
- all_blocks excluded

Reduction from the previous 240-image dataset:
- 10 images per class were removed (40 total).
- Removal was based on the lowest object-region sharpness score (variance of Laplacian) among the already curated/labeled 60 images per class.
- Bounding boxes and labels of the retained images are unchanged.

Recommended split:
- Train 70% = 140 total = 35 per class
- Validation 20% = 40 total = 10 per class
- Test 10% = 20 total = 5 per class

Folders:
images/          200 input images
labels/          200 YOLO .txt annotations
cek_visual/      200 visual QA images with bounding boxes
classes.txt      class ID order
labeling_report_200.csv
removed_40_lowest_sharpness.csv

YOLO label format:
<class_id> <x_center> <y_center> <width> <height>
Coordinates are normalized to 0..1.
