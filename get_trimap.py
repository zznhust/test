import sys
import cv2
import numpy as np
from PIL import Image
import os
from tqdm import tqdm

root_path = '/data/syf/zz-homework/in-context-matting/datasets/ICM16/alpha'
trimap_path = '/data/syf/zz-homework/in-context-matting/datasets/ICM16/trimap'

for img in tqdm(os.listdir(root_path)):
    # 加载mask图像
    image_path = os.path.join(root_path, img)

    # 使用OpenCV读取图像，IMREAD_UNCHANGED参数保证Alpha通道不会被忽略
    # image_with_alpha = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    image = cv2.imread(image_path, flags=1)
    mask = image[:, :, 0]

    for i in range(image.shape[0]):  # 外层循环遍历行
        for j in range(image.shape[1]):  # 内层循环遍历当前行的列
            if mask[i][j] > 0:
                mask[i][j] = 255
                mask[i][j] = 255
                mask[i][j] = 255

    # 定义膨胀与侵蚀的核大小，例如3x3的核
    kernel_size = 30
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # 执行膨胀操作
    dilated_mask = cv2.dilate(mask, kernel, iterations=1)

    # 执行侵蚀操作
    eroded_mask = cv2.erode(mask, kernel, iterations=1)

    # 生成trimap
    # 假设mask中非零值代表前景，我们可以直接用dilated_mask作为前景，eroded_mask保持背景为黑，
    # 然后将两者之外的区域（即原mask中为0但在dilated_mask中不为0的部分）设为灰色（例如128）
    # trimap = np.where(eroded_mask != 0, 255, np.where(dilated_mask == 0, 0, 128))
    trimap = np.zeros((image.shape[0], image.shape[1]))
    for i in range(image.shape[0]):  # 外层循环遍历行
        for j in range(image.shape[1]):  # 内层循环遍历当前行的列
            if dilated_mask[i][j] == 0:
                trimap[i][j] = 0
            elif dilated_mask[i][j] == 255 and eroded_mask[i][j] == 0:
                trimap[i][j] = 128
            else:
                trimap[i][j] = 255

    trimap_array = np.dstack((trimap, trimap, trimap))
    trimap_image = Image.fromarray(trimap_array.astype('uint8'), 'RGB')
    trimap_image.save(os.path.join(trimap_path, img))
