import cv2
from pds4_tools import pds4_read
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from PIL import Image
import os
from skimage import exposure
from skimage import data
import colour
from tqdm import tqdm
from colour_demosaicing import (
    demosaicing_CFA_Bayer_bilinear,
    demosaicing_CFA_Bayer_Malvar2004,
    demosaicing_CFA_Bayer_Menon2007,
    mosaicing_CFA_Bayer)
cctf_encoding = colour.cctf_encoding
_ = colour.utilities.filter_warnings()


class LunarData:

    def __init__(self):

        pass

    def create_dir(self, dir):
        # 创建文件夹
        if not os.path.exists(dir):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(dir)

class LunarDataTCAM(LunarData):

    def __init__(self):
        super().__init__()
        # self.root_dir = root_dir

    def read_and_save(self, file_list, save_path):

        for file in tqdm(file_list):
            if os.path.exists(save_path + file[:-4] + '.png'):
                print(f'{file}存在')
                continue
            d = pds4_read(file, quiet=True)
            img = np.array(d[0].data)
            img = Image.fromarray(img)
            img.save(save_path + file[:-4]+'.png')

class LunarDataPCA(LunarData):

    def __init__(self):
        super().__init__()
        # self.root_dir = root_dir

    def read_and_save(self, file_list, save_path):

        for file in tqdm(file_list):

            if os.path.exists(save_path + file[:-4] + '.png'):
                print(f'{file}存在')
                continue

            d = pds4_read(file, quiet=True)
            img = np.array(d[0].data)
            # img = img / 1023

            img = img.astype(np.float32)

            img = cctf_encoding(demosaicing_CFA_Bayer_bilinear(img,'RGGB'))
            p2, p98 = np.percentile(img, (2, 98))
            img = exposure.rescale_intensity(img,in_range=(p2, p98))
            img = img * 255.0
            # cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = Image.fromarray(np.uint8(img))
            # 保存彩色图像
            # print(save_path + file[:-4] + '.png')
            # cv2.imwrite(save_path + file[:-4] + '.png', img)
            # cv2.imencode('.png', img)[1].tofile(save_path + file[:-4] + '.png')  # 保存带中文路径的图片

            # cv2.imwrite('data\\嫦娥四号\\全景相机\\CE4_GRAS_PCAML-C-053_SCI_N_20230615051405_20230615051405_0296_B.png', img * 255.0)
            img.save(save_path + file[:-4] + '.png')
            # plt.imshow(img)
            # plt.show()

model_list = {
    'ldtcam': LunarDataTCAM,
    'pcaml': LunarDataPCA
}



if __name__ == "__main__":

    t = ["嫦娥四号", '嫦娥五号']

    config_list = {
        "嫦娥四号":
            {
            'root_dir': ['嫦娥四号\\全景相机','嫦娥四号\\地形地貌相机'],
            'type': ['全景相机', '地形地貌相机'],
            'model': ['pcaml', 'ldtcam'],
            'save_root_dir': 'data\\'
            },
        '嫦娥五号':
            {
                'root_dir': ['嫦娥五号\\全景相机'],
                'type': ['全景相机'],
                'model': ['pcaml'],
                'save_root_dir': 'data\\'
            }
    }

    # 获取所有 L 文件
    for ta in t:
        c = config_list[ta]
        for idx in range(len(c['type'])):

            # 图像从该文件夹中读出
            rdir = c['root_dir']
            model = model_list[c["model"][idx]]()
            save_path = os.path.join(c['save_root_dir'], ta, c['type'][idx])

            file_list = os.listdir(rdir[idx]) # 获取文件夹下所有文件名

            # 选择所有 L结尾的文件
            fk = []

            for file in file_list:
                if file[-1] == 'L':
                    fk.append(os.path.join(rdir[idx], file))

            # 创建保存文件夹
            model.create_dir(save_path)
            print(f"处理{ta + c['type'][idx]}")
            model.read_and_save(fk, c['save_root_dir'])


    # file_list = [
    #     'CE4_GRAS_TCAM-I-144_SCI_N_20190111195711_20190111195711_0009_A.2CL'
    # ]
    #
    # ldtcam = LunarDataTCAM('嫦娥三号/地形地貌相机')
    #
    # ldtcam.read_and_save(file_list)
    #
    #
    #
    # file_list = [
    #     'CE4_GRAS_PCAML-C-051_SCI_N_20230615051107_20230615051107_0296_B.2BL'
    # ]
    #
    # pcaml = LunarDataPCA("嫦娥四号/全景相机")
    #
    # pcaml.read_and_save(file_list)

# path = 'CE4_GRAS_TCAM-I-144_SCI_N_20190111195711_20190111195711_0009_A.2CL'
# d = pds4_read(path, quiet=True)
# # fig, axes = plt.subplots(1,1,figsize=(10,10))
# img = np.array(d[0].data)
# plt.imshow(img)
#
# plt.show()