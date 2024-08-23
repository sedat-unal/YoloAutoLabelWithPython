import cv2
import os
import uuid
import glob

from app.app.helpers import *
from app.app.yolo_rotate import yoloRotatebbox


def get_input_data(input_folder: str = None):
    input = os.path.join(input_folder, "*.jpg")
    files = glob.glob(input)
    file_list = []
    for file in files:
        temp = file.split("\\")
        temp_path = temp[-2] + "/" + temp[-1]
        file_list.append(temp_path)
    return file_list


def core(input_img_path: str = None, output_path: str = None, max_angle: int = 0, rotate_angle: int = 0):
    image_name = input_img_path.split('.')[0]
    image_ext = '.' + input_img_path.split('.')[1]

    salt_image_name = output_path + "/" + image_name.split('/')[1]

    for angle in range(0, max_angle, rotate_angle):

        unique_name = str(uuid.uuid4())

        im = yoloRotatebbox(image_name, image_ext, angle)

        bbox = im.rotateYolobbox()
        image = im.rotate_image()

        # to write rotateed image to disk
        cv2.imwrite(salt_image_name + '_' + unique_name + '_' + str(angle) + '.jpg', image)

        file_name = salt_image_name + '_' + unique_name + '_' + str(angle) + '.txt'
        if os.path.exists(salt_image_name):
            os.remove(salt_image_name)

        # to write the new rotated bboxes to file
        for i in bbox:
            with open(file_name, 'a') as fout:
                fout.writelines(
                    ' '.join(
                        map(str, cvFormattoYolo(i, im.rotate_image().shape[0], im.rotate_image().shape[1]))) + '\n')
