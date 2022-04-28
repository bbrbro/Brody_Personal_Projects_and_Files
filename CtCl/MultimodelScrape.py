from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import chromedriver_binary
import time

if False:
    url = 'https://microscope.openai.com/models/contrastive_4x/image_block_4_5_Add_6_0?models.op.feature_vis.type=channel&models.op.technique=feature_vis'
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    driver.fullscreen_window()
    driver.execute_script("document.body.style.zoom='25%'")
    time.sleep(60)
    data = driver.find_elements(by=By.ID, value='img')

    for item in data:
        print(item['src'])

if False:
    image_url_1="https://oaiggoh.blob.core.windows.net/microscopeprod/2020-07-25/2020-07-25/contrastive_16x/lucid.feature_vis/_feature_vis/alpha%3DFalse%26negative%3DFalse%26objective%3Dchannel%26op%3Dimage_block_3%252F0%252FAdd_8%253A0%26repeat%3D0%26start%3D"
    set_1=[str(i) for i in range(0,1530, 32) for _ in range(32)]
    image_url_2="%26steps%3D4096%26stop%3D"
    set_2=[str(i) for i in range(32,1538, 32) for _ in range(32)]
    image_url_3="/channel-"

    image_url_list = [image_url_1 + string_1 + image_url_2 + string_2 + image_url_3 for string_1, string_2 in zip(set_1, set_2)]

    saving_path="C:/Users/brody.westberg/OneDrive - Thermo Fisher Scientific/Documents/OpenAIDream/"
    image_addendum = [str(num) for num in range(1535)]
    image_suffix = ".png"

    image_list = [image_url + addendum + image_suffix for image_url, addendum in zip(image_url_list, image_addendum)]
    image_names = [saving_path + addendum + image_suffix for addendum in image_addendum]

    for image, name in zip(image_list,image_names):
        print(image)
        print(name)
        urllib.request.urlretrieve(image, name)

if False:
    import cv2
    import os


    image_folder = "C:/Users/brody.westberg/OneDrive - Thermo Fisher Scientific/Documents/OpenAIDream/"
    video_name = 'C:/Users/brody.westberg/OneDrive - Thermo Fisher Scientific/Documents/OpenAIDream/Dream.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 8, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()