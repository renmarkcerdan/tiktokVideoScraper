from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import os
from urllib.request import urlopen

def downloadVideo(link, id):
    print(f"Downloading video {id} from: {link}")
    cookies = {
        '_ga': 'GA1.1.164127295.1709687532',
        '__gads': 'ID=ff9d7944fdd31129:T=1709687568:RT=1709687568:S=ALNI_MZJN109tWg65GQWbTisgRSnM5froQ',
        '__gpi': 'UID=00000d28dc2d4028:T=1709687568:RT=1709687568:S=ALNI_MZ84Za1BA3Q-j7g5VHwYTUGbjm3YQ',
        '__eoi': 'ID=0335a47892b64fea:T=1709687568:RT=1709687568:S=AA-AfjY4KBhHQhOChFd2KmyoOHOv',
        'FCNEC': '%5B%5B%22AKsRol-180sg7FCeLORAZW2pdT8q3lSaL5216k7Bg4lK4tkJ4i0FOPFUMEBHp0H46cKW0eQu-RqxzhSO-Kggy03_YL3PUT9EnxffshK5BSN1HwH3mHn9fde1-HstugD8JlDeVCj29lra0Ct3w-D0FR7zzsI0yHAf2w%3D%3D%22%5D%5D',
        '_ga_ZSF3D6YSLC': 'GS1.1.1709687532.1.0.1709688339.0.0.0',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-PH,en-US;q=0.9,en;q=0.8',
        # 'cookie': '_ga=GA1.1.164127295.1709687532; __gads=ID=ff9d7944fdd31129:T=1709687568:RT=1709687568:S=ALNI_MZJN109tWg65GQWbTisgRSnM5froQ; __gpi=UID=00000d28dc2d4028:T=1709687568:RT=1709687568:S=ALNI_MZ84Za1BA3Q-j7g5VHwYTUGbjm3YQ; __eoi=ID=0335a47892b64fea:T=1709687568:RT=1709687568:S=AA-AfjY4KBhHQhOChFd2KmyoOHOv; FCNEC=%5B%5B%22AKsRol-180sg7FCeLORAZW2pdT8q3lSaL5216k7Bg4lK4tkJ4i0FOPFUMEBHp0H46cKW0eQu-RqxzhSO-Kggy03_YL3PUT9EnxffshK5BSN1HwH3mHn9fde1-HstugD8JlDeVCj29lra0Ct3w-D0FR7zzsI0yHAf2w%3D%3D%22%5D%5D; _ga_ZSF3D6YSLC=GS1.1.1709687532.1.0.1709688339.0.0.0',
        'referer': 'https://www.google.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'S2pkV0Rk', # NOTE: This value gets changed, please use the value that you get when you copy the curl command from the network console
    }
    
    print("STEP 4: Getting the download link")
    print("If this step fails, PLEASE read the steps above")
    response = requests.post('https://ssstik.io/abc?url=dl', cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    data_path = os.path.join(dir_path, "tiktokVideoScraper/videos/")
    video = os.path.join(data_path, f"{videoTitle}.mp4")
    print("STEP 5: Saving the video :)")

    mp4File = urlopen(downloadLink)
    print(f"{mp4File}")
    # Feel free to change the download directory
    with open(f"{video}", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

print("STEP 1: Open Chrome browser")
options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)
# Change the tiktok link
driver.get("https://www.tiktok.com/@realexotichandsome")

# IF YOU GET A TIKTOK CAPTCHA, CHANGE THE TIMEOUT HERE
# to 60 seconds, just enough time for you to complete the captcha yourself.
time.sleep(60)

scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

print("STEP 2: Scrolling page")
while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break 

# this class may change, so make sure to inspect the page and find the correct class
className = "e1cg0wnj1"

script  = "let l = [];"
script += "document.getElementsByClassName(\""
script += className
script += "\").forEach(item => { l.push(item.querySelector('a').href)});"
script += "return l;"

urlsToDownload = driver.execute_script(script)

print(f"STEP 3: Time to download {len(urlsToDownload)} videos")
for index, url in enumerate(urlsToDownload):
    print(f"Downloading video: {index}")
    downloadVideo(url, index)
    time.sleep(10)
