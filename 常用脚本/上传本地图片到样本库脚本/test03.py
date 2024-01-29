import os
import shutil
import xml.etree.ElementTree as ET

def del_inxml_noobj_file(src_folder,dst_folder):
    for filename in os.listdir(src_folder):
        if filename.endswith('.xml'):
            xml_path = os.path.join(src_folder,filename)

            tree = ET.parse(xml_path)
            root = tree.getroot()

            obj_nodes = root.findall('.//object')
            if len(obj_nodes) == 0:
                dst_path = os.path.join(dst_folder,filename)
                shutil.move(xml_path,dst_path)
                print(f'Moved {filename} to {dst_folder}')

src_folder = r'H:\潘秉宏\重新标注样本\待上传样本库样本_12-18_(7-3至8-4)'
dst_folder = r'H:\潘秉宏\重新标注样本\待上传样本库样本_12-18_(7-3至8-4)\xmls'

del_inxml_noobj_file(src_folder,dst_folder)