from lib2to3.pgen2 import driver
import os
import platform
import re
import math
import csv
from time import sleep
from unittest import result
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from original_logger import OriginalLogger
from crawler.saunaikitai_detail_crawler import SaunaikitaiDetailCrawler

class SaunaikitaiCrawler:
    SAUNA_SEARCH_URL = 'https://sauna-ikitai.com/search?prefecture[]=hokkaido&prefecture[]=aomori&prefecture[]=iwate&prefecture[]=miyagi&prefecture[]=akita&prefecture[]=yamagata&prefecture[]=fukushima&prefecture[]=ibaraki&prefecture[]=tochigi&prefecture[]=gunma&prefecture[]=saitama&prefecture[]=chiba&prefecture[]=tokyo&prefecture[]=kanagawa&prefecture[]=niigata&prefecture[]=toyama&prefecture[]=ishikawa&prefecture[]=fukui&prefecture[]=yamanashi&prefecture[]=nagano&prefecture[]=gifu&prefecture[]=shizuoka&prefecture[]=aichi&prefecture[]=mie&prefecture[]=shiga&prefecture[]=kyoto&prefecture[]=osaka&prefecture[]=hyogo&prefecture[]=nara&prefecture[]=wakayama&prefecture[]=tottori&prefecture[]=shimane&prefecture[]=okayama&prefecture[]=hiroshima&prefecture[]=yamaguchi&prefecture[]=tokushima&prefecture[]=kagawa&prefecture[]=ehime&prefecture[]=kochi&prefecture[]=fukuoka&prefecture[]=saga&prefecture[]=nagasaki&prefecture[]=kumamoto&prefecture[]=oita&prefecture[]=miyazaki&prefecture[]=kagoshima&prefecture[]=okinawa&ordering=ikitai_counts_desc'
    SAUNA_SEARCH_URL_FORMAT = 'https://sauna-ikitai.com/search?ordering=ikitai_counts_desc&page={0}&prefecture[]=aichi&prefecture[]=akita&prefecture[]=aomori&prefecture[]=chiba&prefecture[]=ehime&prefecture[]=fukui&prefecture[]=fukuoka&prefecture[]=fukushima&prefecture[]=gifu&prefecture[]=gunma&prefecture[]=hiroshima&prefecture[]=hokkaido&prefecture[]=hyogo&prefecture[]=ibaraki&prefecture[]=ishikawa&prefecture[]=iwate&prefecture[]=kagawa&prefecture[]=kagoshima&prefecture[]=kanagawa&prefecture[]=kochi&prefecture[]=kumamoto&prefecture[]=kyoto&prefecture[]=mie&prefecture[]=miyagi&prefecture[]=miyazaki&prefecture[]=nagano&prefecture[]=nagasaki&prefecture[]=nara&prefecture[]=niigata&prefecture[]=oita&prefecture[]=okayama&prefecture[]=okinawa&prefecture[]=osaka&prefecture[]=saga&prefecture[]=saitama&prefecture[]=shiga&prefecture[]=shimane&prefecture[]=shizuoka&prefecture[]=tochigi&prefecture[]=tokushima&prefecture[]=tokyo&prefecture[]=tottori&prefecture[]=toyama&prefecture[]=wakayama&prefecture[]=yamagata&prefecture[]=yamaguchi&prefecture[]=yamanashi'
    SAUNA_DETAIL_URL_PATTERN = r'https:\/\/sauna-ikitai.com\/saunas\/[0-9]+'
    FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image/screen.png")
    DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/sauna_data.csv")
    
    # １ページの最大表示数
    MAX_PAGE_CONTENTS = 20
    
    
    def __init__(self):
        # Loggerの生成
        self.logger = OriginalLogger()
        
        
    def crawl(self):
        # chromedriverの設定
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        # MEMO: この辺りの設定で20件のデータ抽出で10秒早くなる
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
        
        # timeout対策
        # https://qiita.com/ssbb/items/306ec9a1dbecd77d001b
        # https://stackoverflow.com/questions/48450594/selenium-timed-out-receiving-message-from-renderer
        options.add_argument("start-maximized")
        options.add_argument("enable-automation")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-infobars")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        
        # Raspberry piの場合独自のdriverに
        if platform.node() == 'raspberrypi':
            driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
        else:
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        
        # find_elementの際、要素が見つかるまで指定した最大時間待機
        driver.implicitly_wait(5)
        
        try:
            # 検索結果画面を開く
            driver.get(SaunaikitaiCrawler.SAUNA_SEARCH_URL_FORMAT.format(1))

            self.logger.info("Search result screen display completed!")

            # 検索結果数を取得
            ## MEMO: XPATHで取れなかったので、仕方なく結果から数値だけとる
            result_number_text = driver.find_element(by=By.CLASS_NAME, value='p-result_number').text
            result_number = re.sub(r"\D", "", result_number_text)
            
            # 最大ページ数を計算
            total_pages_number = math.ceil(int(result_number) / self.MAX_PAGE_CONTENTS)

            self.logger.info("Search Result: " + result_number)
            self.logger.info("Number of page content: " + str(self.MAX_PAGE_CONTENTS))
            self.logger.info("Toral Pages: " + str(total_pages_number))
            
            # csvファイル指定
            with open(self.DATA_FILE_PATH, 'w') as f:
                writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                
                csv_header = ['イキタイ', 'サ活', 'サウナ飯', 'ターゲット', '市区町村', '施設名', '施設タイプ', '住所', 'TEL', 'HP', '定休日', '営業時間', '料金', 'URL', 'CREATE_AT', '緯度', '経度']
                writer.writerow(csv_header)
                
                #  全てのページを読み終わるまでループする
                for i in range(total_pages_number):
                    
                    driver.get(SaunaikitaiCrawler.SAUNA_SEARCH_URL_FORMAT.format(i + 1))
                    
                    # ページ中のリンクを取得する
                    self.logger.info("###############################################")
                    self.logger.info("Start Sauna Search Page : {0}".format(i + 1))
                    all_links =  driver.find_elements(by=By.XPATH, value='//a[@href]')
                    
                    # サウナ施設情報リスト
                    sauna_info_list = []
                    # サウナ施設URLリスト
                    sauna_detail_links = []
                    
                    # サウナ施設ページのリンクだけ抽出
                    for link in all_links:
                        link_text = link.get_attribute("href")
                        if re.fullmatch(self.SAUNA_DETAIL_URL_PATTERN, link_text):
                            sauna_detail_links.append(link_text)
                    
                    # 取得した施設詳細リンクから施設情報を取得
                    for detail_link in sauna_detail_links:
                        detail_crawler = SaunaikitaiDetailCrawler()
                        sauna_info_list.append(detail_crawler.crawl(detail_link))
                    
                    # 1ページ単位で書き込み
                    writer.writerows(sauna_info_list)
                    self.logger.info("Completed writing {0} lines to csv file".format(len(sauna_info_list)))
                    
                    self.logger.info("End Sauna Search Page : {0}".format(i + 1))
                
            

        except NoSuchElementException as e:
            self.logger.error("NoSuchElementException!!")
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
        
        self.logger.info(self.FILENAME)
        
        # chromedriverのclose
        # driverの操作を完全に終えてからcloseすること
        driver.close()
        driver.quit()
        
        