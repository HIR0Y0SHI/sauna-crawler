from audioop import add
from lib2to3.pgen2 import driver
import os
from pydoc import cli
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from original_logger import OriginalLogger
from client.geocoding_client import GeocodingClient

class SaunaikitaiDetailCrawler:
    
    FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image/detail.png")

    
    def __init__(self):
         # Loggerの生成
        self.logger = OriginalLogger()
        
    # url: サウナイキタイの施設ページ
    # 例) https://sauna-ikitai.com/saunas/4393
    def crawl(self, url):
        # chromedriverの設定
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')                             
        options.add_argument('--proxy-server="direct://"')         
        options.add_argument('--proxy-bypass-list=*')              
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--lang=ja')                          
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--log-level=3")
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        
        # find_elementの際、要素が見つかるまで指定した最大時間待機
        driver.implicitly_wait(5)
        
        sauna_info = []
        
        try:
            #施設ページを開く
            self.logger.info(url)
            driver.get(url)

            self.logger.info("Start analysis of facility page!")
            
            # ユーザ評価
            ## イキタイ
            ikitai_count = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > header > div.p-saunaDetailHeader_action > div.p-action.p-action--ikitai.js-ikitai > div.p-action_number.js-ikitaiCounter').text
            sauna_info.append(ikitai_count)
            ## サ活
            sakatsu_count = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > nav > div.p-localNav_content.js-swipeScrollContent > ul > li:nth-child(2) > a > span > span').text
            sauna_info.append(sakatsu_count)
            ## サウナ飯
            sameshi_count = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > nav > div.p-localNav_content.js-swipeScrollContent > ul > li:nth-child(3) > a > span > span').text
            sauna_info.append(sameshi_count)

            # 基本情報
            ## ターゲット（男女, 男）
            target = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > header > div.p-saunaDetailHeader_main > p.p-saunaDetailHeader_target').text
            sauna_info.append(target)
            ## 市区町村
            city = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > header > div.p-saunaDetailHeader_main > p.p-saunaDetailHeader_area').text
            sauna_info.append(city)
            ## 施設名
            sauna_name = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > div.p-saunaDetailBody > div.p-saunaDetailShop > div > div.p-saunaDetailShop_info > table > tbody > tr:nth-child(1) > td').text
            sauna_info.append(sauna_name)
            ## 施設タイプ
            type = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > div.p-saunaDetailBody > div.p-saunaDetailShop > div > div.p-saunaDetailShop_info > table > tbody > tr:nth-child(2) > td').text
            sauna_info.append(type)
            ## 住所
            address = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > div.p-saunaDetailBody > div.p-saunaDetailShop > div > div.p-saunaDetailShop_info > table > tbody > tr:nth-child(3) > td').text
            sauna_info.append(address)
            ## TEL
            tel = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > div.p-saunaDetailBody > div.p-saunaDetailShop > div > div.p-saunaDetailShop_info > table > tbody > tr:nth-child(6) > td').text
            sauna_info.append(tel)
            ## HP
            hp = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > div.p-saunaDetailBody > div.p-saunaDetailShop > div > div.p-saunaDetailShop_info > table > tbody > tr:nth-child(7) > td').text
            sauna_info.append(hp)
            ## 定休日
            regular_holiday = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > div.p-saunaDetailBody > div.p-saunaDetailShop > div > div.p-saunaDetailShop_info > table > tbody > tr:nth-child(8) > td').text
            sauna_info.append('\\n'.join(regular_holiday.splitlines())) # 改行コードを置換
            ## 営業時間
            business_hours = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > div.p-saunaDetailBody > div.p-saunaDetailShop > div > div.p-saunaDetailShop_info > table > tbody > tr:nth-child(9) > td').text
            sauna_info.append('\\n'.join(business_hours.splitlines())) # 改行コードを置換
            ## 料金
            price = driver.find_element(by=By.CSS_SELECTOR, value='body > div.l-page > div.l-containers.js-containers > div:nth-child(1) > article > div.p-saunaDetailBody > div.p-saunaDetailShop > div > div.p-saunaDetailShop_info > table > tbody > tr:nth-child(10) > td').text
            sauna_info.append('\\n'.join(price.splitlines())) # 改行コードを置換
            
            # URL
            sauna_info.append(url)
            # 時間
            create_at = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
            sauna_info.append(create_at)
            
            # 緯度経度の取得
            location = self.get_location(sauna_name, address)
            ## 緯度
            sauna_info.append(location[0])
            ## 経度
            sauna_info.append(location[1])
            

            self.logger.info("===== Sauna INFO [" + sauna_name + "] =====")
            self.logger.debug("イキタイ: " + ikitai_count)
            self.logger.debug("サ活: " + sakatsu_count)
            self.logger.debug("サ飯: " + sameshi_count)
            self.logger.debug("施設タイプ: " + type)
            self.logger.debug("施設名: " + sauna_name)
            self.logger.debug("住所:" + address)
            self.logger.debug("TEL: " + tel)
            self.logger.debug("HP: " + hp)
            self.logger.debug("定休日: " + regular_holiday)
            self.logger.debug("営業時間: " + business_hours)
            self.logger.debug("料金:" + price)
            self.logger.debug("緯度:" + location[0])
            self.logger.debug("経度:" + location[1])
            self.logger.debug("====================================================")
            

        except NoSuchElementException as e:
            self.logger.error("NoSuchElementException!! ")
            self.logger.info("Error File : {}".format(__file__))
            self.logger.info(e)
        except Exception as e:
            self.logger.error("Unknown error!!")
            self.logger.info("Error File : {}".format(__file__))
            self.logger.info(e)
            
        self.logger.info("Analysis completed!")
        
        
        
        # get width and height of the page
        w = driver.execute_script("return document.body.scrollWidth;")
        h = driver.execute_script("return document.body.scrollHeight;")

        # set window size
        driver.set_window_size(w,h)

        # Get Screen Shot
        # driver.save_screenshot(self.FILENAME)
        # self.logger.info(self.FILENAME)
        
        # chromedriverのclose
        # driverの操作を完全に終えてからcloseすること
        driver.close()
        driver.quit()
        
        return sauna_info
    
    
    # 緯度経度を取得する
    def get_location(self, sauna_name, address):
        client = GeocodingClient()
        location = client.request(sauna_name)
        
        lat = ''
        lng = ''
        
        # まずは施設名から取得
        if location is not None:
            return (location[0], location[1])
        
        self.logger.warn("Failure to obtain location information by sauna name. [{}]".format(sauna_name))
        
        # 施設名で失敗した時は住所で
        location = client.request(address)
        if location is not None:
            return (location[0], location[1])
        
        self.logger.error("Failure to obtain location information by address. [{}]".format(address))
        
        return (lat, lng)
        
        