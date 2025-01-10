import os
import json

# ICM16 数据集路径（相对路径）
dataset_path = 'ICM16-image'  # 数据集路径
json_output_path = 'ICM16.json'  # JSON 文件输出路径

# 初始化字典存储数据
dataset = {}

# 遍历 ICM16 数据集目录
for root, _, files in os.walk(dataset_path):
    for file in files:
        if file.endswith(('.png', '.jpg', '.jpeg')):  # 过滤图像文件
            file_path = os.path.join(root, file)
            file_name = os.path.splitext(file)[0]  # 获取文件名，不带扩展名

            # 解析 class 信息
            class_name, _ = file_name.split('_', 1)  # 分割文件名获取 class 部分

            # 构建数据条目
            data_entry = {
                "dataset_name": "ICM",
                "class": class_name,  # 从文件名解析出的 class
                "sub_class": None,
                "HalfOrFull": None,
                "TransparentOrOpaque": None,
                "source": "dreambooth",
                "type": "instance"
            }

            # 将数据条目添加到字典中
            dataset[file_name] = data_entry

# 写入 JSON 文件
with open(json_output_path, 'w') as json_file:
    json.dump(dataset, json_file, indent=4)

print(f"ICM16 数据集 JSON 文件已保存至 {json_output_path}")