import os
print('开始修改！！！')
dst_path = 'H:\pbh\重新标注样本\VOCdevkit4含26-27-28-29\images'

for root,dirs,files, in os.walk(dst_path):
    for file_name in files:
        if "..jpg" in file_name:
            new_name = file_name.replace("..jpg",".jpg")
            os.rename(os.path.join(root,file_name),os.path.join(root,new_name))
print('修改完毕！！！')