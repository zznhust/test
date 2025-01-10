# json文件说明

ICM57数据集文件夹中包含数据集的json文件，而我扩展的ICM16数据集中未包含json文件

没有包含json文件的数据集无法在项目中跑通，所以我们需要为ICM16数据集也配置一个json文件

查看ICM57的json文件配置格式，我设计了一个获得数据集ICM16的json文件的脚本如下：

``````python
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
``````

注意：该脚本对命名为“类别_标号”的imge-alpha数据集生成json文件具有通用性