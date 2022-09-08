import urllib.request
from urllib.request import Request
import xml.etree.ElementTree as ET
from original_logger import OriginalLogger


class GeocodingClient:
  
  GEOCODING_URL = 'https://www.geocoding.jp/api/'
  
  def __init__(self):
    # Loggerの生成
    self.logger = OriginalLogger()
    
  def request(self, query):
    # リクエストパラメータ
    params = {
      'q': query
    }
    
    # Requestの生成
    url_params = '{}?{}'.format(self.GEOCODING_URL, urllib.parse.urlencode(params))
    req = Request(url=url_params, method='GET')
    
    geocoding_result = ''
    lat = ''
    lng = ''
    
    self.logger.info("Start Geocoding HTTP Request [{}]".format(query))
    
    try:
      # HTTPリクエスト
      with urllib.request.urlopen(req) as response:
        
        # レスポンス（XML）を解析
        geocoding_result = response.read()
        root = ET.fromstring(geocoding_result)
        coordinate = root.findall('coordinate')
        
        self.logger.info("Completed Geocoding HTTP Request [{}]".format(query))
             
        # 緯度、経度だけ取得
        for co in coordinate:
          # 緯度
          lat = co.find("lat").text
          # 経度
          lng = co.find("lng").text
        
        # 緯度経度をタプルで返却
        return (lat, lng)
          
    except urllib.error.URLError as e:
      self.logger.error("URLError!!")
      self.logger.info(e)
      pass
      
    except Exception as e:
      self.logger.error("Unknown error!!")
      self.logger.info(e)
      pass
    
    
    return None
