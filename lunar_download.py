import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os
import math
import shutil
from tqdm import tqdm
import wget

class LunarDownload:

    def __init__(self, root_dir, is_o = True, username = '', password = ''):

        self.root_dir = root_dir
        # self.config = config


        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument(config["chrome_options"])
        # 忽略证书错误
        chrome_options.add_argument('--ignore-certificate-errors')
        # 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 忽略 DevTools listening on ws://127.0.0.1... 提示
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        if is_o:
            self.driver.get("https://moon.bao.ac.cn/ce5web/searchOrder_dataSearchData.search")
            time.sleep(3)
            self.login(username, password)

    def login(self, username, password):

        self.driver.find_element(by="xpath", value='//*[@id="user"]/div[1]/span').click()
        time.sleep(1)
        self.driver.find_element(by='xpath', value='//*[@id="uesrname"]').send_keys(username)
        self.driver.find_element(by='xpath', value='//*[@id="password"]').send_keys(password)
        self.driver.find_element(by="xpath", value='//*[@id="loginBtn"]').click()

        print("登录成功")

    def make_type_dir(self, name):

        if not os.path.exists(os.path.join(self.root_dir, name)):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(os.path.join(self.root_dir, name))


    def download_from_config(self,config):


        # if not os.path.exists(os.path.join(self.root_dir,config["name"])):  # 判断是否存在文件夹如果不存在则创建为文件夹
        #     os.makedirs(folder_path)
        '''
            config = {
                "name": "嫦娥四号",
                "cxpath": '//*[@id="starRow"]/form/ul/li[7]/label/span[4]',
                "download_type": ['全景相机', '地形地貌相机'],
                "txpath": ['//*[@id="cameraRow"]/form/ul/li[4]/label', '//*[@id="cameraRow"]/form/ul/li[2]/label']
            }
            '//*[@id="gridcolumn-1119-textEl"]'

            '//*[@id="addListToCar-btnInnerEl"]'

            '//*[@id="collect"]'

            //*[@id="tableview-1092-record-31"]/tbody/tr/td[2]/div/div/div[2]/div[2]/div[4]
            //*[@id="tableview-1092-record-31"]/tbody/tr/td[2]/div/div/div[2]/div[2]/div[4]
        '''
        for idx in range(len(config["download_type"])):
            type = config["download_type"][idx]
            # if not os.path.exists(os.path.join(self.root_dir,config["name"], type)):  # 判断是否存在文件夹如果不存在则创建为文件夹
            #     os.makedirs(os.path.join(self.root_dir,config["name"], type))

            # 先点 嫦娥四号标签 然后点全景相机标签 然后点小框 然后点加入收藏夹 然后进入收藏夹
            self.driver.find_element(by="xpath", value=config["cxpath"]).click()
            self.driver.find_element(by="xpath", value=config["txpath"][idx]).click()
            print(f"进入了{type}")
            for k in range(config["n"]):
                time.sleep(3)
                self.driver.find_element(by="class name", value='x-column-header-text-wrapper').click()
                self.driver.find_element(by="xpath", value='//*[@id="addListToCar-btnInnerEl"]').click()
                # 在这里需要翻页继续上面的操作
                button_list = self.driver.find_elements(by="class name", value='x-btn.x-unselectable.x-box-item.x-toolbar-item.x-btn-default-toolbar-small')
                button_list[2].click()

            self.driver.find_element(by="xpath", value='//*[@id="collect"]').click()
            all_handles = self.driver.window_handles
            origin_h = all_handles[0]
            swi_h = all_handles[1]


            # 切换到相应标签， 将所有全选 导出txt 删除所有 切换回
            self.driver.switch_to.window(swi_h)
            print(self.driver.title)

            # 创建文件夹
            if not os.path.exists(os.path.join("data",config["name"], type)):  # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(os.path.join("data",config["name"], type))
            path = os.path.join("data",config["name"], type)
            all_num = config['n'] * 10

            page_num = int(math.ceil(all_num / 20))
            time.sleep(10)
            for ii in range(page_num):
                # self.driver.find_element(by="class name", value='x-column-header-text-container').click()
                self.driver.find_elements(by="class name", value='x-column-header-text-container')[1].click()
                self.driver.find_elements(by="class name", value='x-column-header-text-container')[0].click()
                self.driver.find_element(by="xpath", value='//*[@id="downLoadButton-btnInnerEl"]').click()
                self.driver.find_element(by="xpath", value='//*[@id="deleteButton-btnInnerEl"]').click()
                time.sleep(10)
                os.rename("C:\\Users\\xiaoc\\Downloads\\downloadResult.txt", f"C:\\Users\\xiaoc\\Downloads\\downloadResult_{ii}.txt")
                try:
                    os.remove(os.path.join(path,f"downloadResult_{ii}.txt"))
                except OSError:
                    pass
                shutil.move(f"C:\\Users\\xiaoc\\Downloads\\downloadResult_{ii}.txt", path)
                print(f"移动完成{ii}")

                # os.remove("C:\\Users\\xiaoc\\Downloads\\downloadResult.txt")
                # os.remove(f"C:\\Users\\xiaoc\\Downloads\\downloadResult_{ii}.txt")
                #
                # print(f"删除downloadResult_{ii}.txt完成")


            self.driver.close()
            self.driver.switch_to.window(origin_h)
            time.sleep(5)

    def download_for_text(self, config):
        '''

        config = {
             "name": "嫦娥三号",
             "cxpath": '//*[@id="starRow"]/form/ul/li[5]/label',
            "download_type": ['全景相机', '地形地貌相机'],
             "txpath": ['//*[@id="cameraRow"]/form/ul/li[5]/label/span[2]',
                        '//*[@id="cameraRow"]/form/ul/li[3]/label'],
            "download_url":[
                    '',
                    ''
            ]
        }

        '''
        '//*[@id="tableview-1092-record-43"]/tbody/tr/td[2]/div/div/div[2]/div[2]/div[1]/div/a'
        '//*[@id="tableview-1092-record-44"]/tbody/tr/td[2]/div/div/div[2]/div[2]/div[1]/div/a'

        # 获取文件名， 文件下载， 文件移动
        for idx in range(len(config["download_type"])):
            type = config["download_type"][idx]
            if not os.path.exists(os.path.join(self.root_dir,config["name"], type)):  # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(os.path.join(self.root_dir,config["name"], type))

            # 先点 嫦娥四号标签 然后点全景相机标签 然后点小框 然后点加入收藏夹 然后进入收藏夹
            self.driver.find_element(by="xpath", value=config["cxpath"]).click()
            self.driver.find_element(by="xpath", value=config["txpath"][idx]).click()
            print(f"进入了{config['name']},{type}")
            time.sleep(5)

            if config['name'] == "嫦娥四号":
                for epoch in range(config['n']):
                    file_list = self.driver.find_elements(by="class name", value="search-item-title")
                    for file in file_list:
                        file_name = file.text

                        download_path = config['download_url'][idx].format(file_name.split('_')[2].split('-')[0]) + file_name

                        if self.check_file_on(os.path.join(self.root_dir,config["name"], type,file_name)):
                            wget.download(download_path,os.path.join(self.root_dir,config["name"], type,file_name))
                            print(download_path)
                            time.sleep(2)
                        else:
                            print(f'存在{file_name}')
                    button_list = self.driver.find_elements(by="class name",
                                                            value='x-btn.x-unselectable.x-box-item.x-toolbar-item.x-btn-default-toolbar-small')
                    button_list[2].click()
                    time.sleep(5)
            elif config['name'] == "嫦娥三号":
                for epoch in range(config['n']):
                    file_list = self.driver.find_elements(by="class name", value="search-item-title")
                    for file in file_list:
                        file_name = file.text
                        if file_name[-2:] == '2A' and type == "全景相机":
                            download_path = config['download_url'][idx][file_name[-2:]].format(
                                file_name.split('_')[2].split('-')[0]) + file_name
                            if self.check_file_on(os.path.join(self.root_dir, config["name"], type, file_name)):
                                wget.download(download_path,
                                              os.path.join(self.root_dir, config["name"], type, file_name))
                                print(download_path)
                                time.sleep(2)
                            else:
                                print(f'存在{file_name}')
                        else:
                            download_path = config['download_url'][idx][file_name[-2:]] + file_name
                            if self.check_file_on(os.path.join(self.root_dir, config["name"], type, file_name)):
                                wget.download(download_path,
                                              os.path.join(self.root_dir, config["name"], type, file_name))
                                print(download_path)
                                time.sleep(2)
                            else:
                                print(f'存在{file_name}')

                    button_list = self.driver.find_elements(by="class name",
                                                            value='x-btn.x-unselectable.x-box-item.x-toolbar-item.x-btn-default-toolbar-small')
                    button_list[2].click()
                    time.sleep(5)

            elif config['name'] == "嫦娥五号":
                for epoch in range(config['n']):
                    file_list = self.driver.find_elements(by="class name", value="search-item-title")
                    for file in file_list:
                        file_name = file.text

                        download_path = config['download_url'][idx].format(file_name.split('_')[2].split('-')[0], file_name.split('_')[2]) + file_name
                        if self.check_file_on(os.path.join(self.root_dir, config["name"], type, file_name)):
                            wget.download(download_path, os.path.join(self.root_dir, config["name"], type, file_name))
                            print(download_path)
                            time.sleep(2)
                        else:
                            print(f'存在{file_name}')
                    button_list = self.driver.find_elements(by="class name",
                                                            value='x-btn.x-unselectable.x-box-item.x-toolbar-item.x-btn-default-toolbar-small')
                    button_list[2].click()
                    time.sleep(5)

    def test(self):

        k = self.driver.find_elements(by="class name", value="search-item-title")
        print(k)

    def check_file_on(self, path):

        if os.path.exists(path):
            return False
        else:
            return True

if __name__ == "__main__":

    n = 20

    downloader = LunarDownload(".\\" , username="xiaoc57", password="Jy20010131")
    downloader.make_type_dir("data")
    # downloader.test()
    configs = [
        {
            "name": "嫦娥三号",
            "n": n,
            "cxpath": '//*[@id="starRow"]/form/ul/li[5]/label',
            "download_type": ['全景相机', '地形地貌相机'],
            "txpath": ['//*[@id="cameraRow"]/form/ul/li[5]/label/span[2]',
                       '//*[@id="cameraRow"]/form/ul/li[3]/label'],
            "download_url": [{
                '2A': 'https://moon.bao.ac.cn/ce5web/cedownload/{}-C/2A/',
                '2B': 'https://moon.bao.ac.cn/ce5web/cedownload/PCAML-C/2B/',
                '2C': 'https://moon.bao.ac.cn/ce5web/cedownload/PCAML-C/2C/'
            },
                {
                    '2A': 'https://moon.bao.ac.cn/ce5web/cedownload/TCAM-I/2A/',
                    '2B': 'https://moon.bao.ac.cn/ce5web/cedownload/TCAM-I/2B/',
                    '2C': 'https://moon.bao.ac.cn/ce5web/cedownload/TCAM-I/2C/'
                }
            ]
                # 'https://moon.bao.ac.cn/ce5web/cedownload/PCAML-C/2C/CE3_BMYK_PCAMR-C-055_SCI_N_20140113195844_20140113195844_0008_A.2C'
                # 'https://moon.bao.ac.cn/ce5web/cedownload/CE4ROLL/CE4/PCAML/C/2B/2023-07/CE4_GRAS_PCAMR-C-055_SCI_N_20230615051647_20230615051647_0296_B.2B'
                # 'https://moon.bao.ac.cn/ce5web/cedownload/CE4ROLL/CE4/PCAMR/C/2B/2023-07/CE4_GRAS_PCAMR-C-055_SCI_N_20230615051647_20230615051647_0296_B.2B'
                # 'https://moon.bao.ac.cn/ce5web/cedownload/CE4ROLL/CE4/{}/C/2B/2023-07/',
                # 'https://moon.bao.ac.cn/ce5web/cedownload/CE4ROLL/CE4/{}/I/2C/2019-03/'
        },
        {
            "name": "嫦娥四号",
            "n": n,
            "cxpath": '//*[@id="starRow"]/form/ul/li[7]/label',
            "download_type": ['全景相机', '地形地貌相机'],
            "txpath": ['//*[@id="cameraRow"]/form/ul/li[4]/label', '//*[@id="cameraRow"]/form/ul/li[2]/label'],
            "download_url": [
                # 'https://moon.bao.ac.cn/ce5web/cedownload/CE4ROLL/CE4/PCAML/C/2B/2023-07/CE4_GRAS_PCAMR-C-055_SCI_N_20230615051647_20230615051647_0296_B.2B'
                # 'https://moon.bao.ac.cn/ce5web/cedownload/CE4ROLL/CE4/PCAMR/C/2B/2023-07/CE4_GRAS_PCAMR-C-055_SCI_N_20230615051647_20230615051647_0296_B.2B'
                'https://moon.bao.ac.cn/ce5web/cedownload/CE4ROLL/CE4/{}/C/2B/2023-07/',
                'https://moon.bao.ac.cn/ce5web/cedownload/CE4ROLL/CE4/{}/I/2C/2019-03/']
        },
        {
            "name": "嫦娥五号",
            "n": n,
            "cxpath": '//*[@id="starRow"]/form/ul/li[9]/label',
            "download_type": ['全景相机'],
            "txpath": ['//*[@id="cameraRow"]/form/ul/li[2]/label'],
            "download_url": [
                'https://moon.bao.ac.cn/ce5web/cedownload/CE5ROLL/{}/{}/2B/202012/'
                # 'CE5-L_GRAS_PCAML-I-008_SCI_N_20201203054903_20201203054903_0004_A.2BL'
            ]
        }
        # 'https://moon.bao.ac.cn/ce5web/cedownload/CE5ROLL/PCAML/PCAML-I-008/2B/202012/CE5-L_GRAS_PCAML-I-008_SCI_N_20201203054903_20201203054903_0004_A.2BL'
    ]

    for config in configs:
        downloader.download_for_text(config)
        # print(os.path.join("data",config_test["name"], '全景相机'))
        time.sleep(3)





