import os
import  shutil
from tqdm import tqdm

def move_mismatched_files(src_folder,dst_img_folder,dst_xml_folder):
    file_list = os.listdir(src_folder)
    progress_bar = tqdm(file_list,desc='Moving Files',unit='file')


    for filename in progress_bar:
        if filename.endswith('.jpg') or filename.endswith('.JPG'):
            xml_file = os.path.join(src_folder,filename[:-4] + '.xml')
            if not os.path.exists(xml_file):
                src_file = os.path.join(src_folder,filename)
                dst_file = os.path.join(dst_img_folder,filename)
                shutil.move(src_file,dst_file)

        elif filename.endswith('.xml'):
            img_file = os.path.join(src_folder,filename[:-4] + '.jpg')
            if not os.path.exists(img_file):
                src_file = os.path.join(src_folder,filename)
                dst_file = os.path.join(dst_xml_folder,filename)
                shutil.move(src_file,dst_file)
                # xml_file = os.path.splitext(filename)[0]+'.xml'
                # xml_file_path = os.path.join(src_folder,xml_file)
                # shutil.move(xml_file_path,dst_folder)
    print('移动完成')



src_folder = r'H:\潘秉宏\重新标注样本\待上传样本库样本_12-18_(7-3至8-4)'
aaa = r'H:\潘秉宏\重新标注样本\待上传样本库样本_12-18_(7-3至8-4)\images'
bbb = r'H:\潘秉宏\重新标注样本\待上传样本库样本_12-18_(7-3至8-4)\xmls'
move_mismatched_files(src_folder,aaa,bbb)