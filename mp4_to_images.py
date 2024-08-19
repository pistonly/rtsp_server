import cv2
from pathlib import Path

input_file = "./DJI_0706.MP4"
target_dir = Path("./tmp")
target_dir.mkdir()

cap = cv2.VideoCapture(input_file)

img_id = 0
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(f"./tmp/{img_id:04d}.jpg", frame)
        img_id += 1
    else:
        break

    if img_id % 100 == 0:
        print(img_id)
