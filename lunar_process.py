from pds4_tools import pds4_read
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from PIL import Image
import os
from skimage import exposure
from skimage import data
import colour

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

class LunarDataTCAM(LunarData):

    def __init__(self, root_dir):
        super().__init__()
        self.root_dir = root_dir

    def read_and_save(self, file_list):

        for file in file_list:

            d = pds4_read(file, quiet=True)
            img = np.array(d[0].data)
            img = Image.fromarray(img)
            img.save(os.path.join(self.root_dir,file[:-4]+'.png'))

class LunarDataPCA(LunarData):

    def __init__(self, root_dir):
        super().__init__()
        self.root_dir = root_dir

    def read_and_save(self, file_list):

        for file in file_list:
            d = pds4_read(file, quiet=True)
            img = np.array(d[0].data)
            # img = img / 1023

            img = img.astype(np.float32)

            img = cctf_encoding(demosaicing_CFA_Bayer_bilinear(img,'RGGB'))
            p2, p98 = np.percentile(img, (2, 98))
            img = exposure.rescale_intensity(img,in_range=(p2, p98))

            img = Image.fromarray(img)
            img.save(os.path.join(self.root_dir, file[:-4] + '.png'))
            # plt.imshow(img)
            # plt.show()



if __name__ == "__main__":

    file_list = [
        'CE4_GRAS_TCAM-I-144_SCI_N_20190111195711_20190111195711_0009_A.2CL'
    ]

    ldtcam = LunarDataTCAM('嫦娥三号/地形地貌相机')

    ldtcam.read_and_save(file_list)



    file_list = [
        'CE4_GRAS_PCAML-C-051_SCI_N_20230615051107_20230615051107_0296_B.2BL'
    ]

    pcaml = LunarDataPCA("嫦娥四号/全景相机")

    pcaml.read_and_save(file_list)

# path = 'CE4_GRAS_TCAM-I-144_SCI_N_20190111195711_20190111195711_0009_A.2CL'
# d = pds4_read(path, quiet=True)
# # fig, axes = plt.subplots(1,1,figsize=(10,10))
# img = np.array(d[0].data)
# plt.imshow(img)
#
# plt.show()