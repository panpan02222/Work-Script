import os
import random
import shutil

# 文件夹路径，图片和标签的根目录
images_dir = 'H:\pbh\重新标注样本\VOCdevkit4含26-27-28-29\images' 
txt_dir = 'H:\pbh\重新标注样本\VOCdevkit4含26-27-28-29\labels'

# 切分比例
TRAIN_RATIO = 0.8

def split_dataset(image_folder, label_folder):
    # 创建保存训练集和验证集的文件夹
    train_image_folder = os.path.join(image_folder, 'train')
    val_image_folder = os.path.join(image_folder, 'val')
    train_label_folder = os.path.join(label_folder, 'train')
    val_label_folder = os.path.join(label_folder, 'val')

    # 判断文件夹是否存在，如果存在则删除并重新创建
    for folder in [train_image_folder, val_image_folder, train_label_folder, val_label_folder]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    # 遍历图片文件夹
    image_files = os.listdir(image_folder)
    random.shuffle(image_files)

    train_size = int(len(image_files) * TRAIN_RATIO)
    train_files = image_files[:train_size]
    val_files = image_files[train_size:]

    # 将图片文件复制到训练集和验证集文件夹中
    for file in train_files:
        src = os.path.join(image_folder, file)
        dst = os.path.join(train_image_folder, file)
        shutil.copy2(src, dst)

    for file in val_files:
        src = os.path.join(image_folder, file)
        dst = os.path.join(val_image_folder, file)
        shutil.copy2(src, dst)

    # 复制对应的标签文件到训练集和验证集文件夹中，并同时记录文件名
    train_label_files = []
    val_label_files = []
    for file in train_files:
        label_file = file.split('.')[0] + '.txt'
        src = os.path.join(label_folder, label_file)
        dst = os.path.join(train_label_folder, label_file)
        train_label_files.append(label_file)
        shutil.copy2(src, dst)

    for file in val_files:
        label_file = file.split('.')[0] + '.txt'
        src = os.path.join(label_folder, label_file)
        dst = os.path.join(val_label_folder, label_file)
        val_label_files.append(label_file)
        shutil.copy2(src, dst)

    # 找到互相不对应的文件并删除
    for label_file in train_label_files:
        if label_file not in train_files:
            os.remove(os.path.join(train_label_folder, label_file))

    for label_file in val_label_files:
        if label_file not in val_files:
            os.remove(os.path.join(val_label_folder, label_file))

    # 统计并打印文件数量
    train_image_count = len(os.listdir(train_image_folder))
    val_image_count = len(os.listdir(val_image_folder))
    train_label_count = len(os.listdir(train_label_folder))
    val_label_count = len(os.listdir(val_label_folder))

    print(f"训练集图片数量: {train_image_count}")
    print(f"验证集图片数量: {val_image_count}")
    print(f"训练集标签数量: {train_label_count}")
    print(f"验证集标签数量: {val_label_count}")

    # return train_image_folder, val_image_folder, train_label_folder, val_label_folder

# 使用示例
split_dataset(images_dir,txt_dir)