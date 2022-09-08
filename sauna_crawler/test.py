import math
import os

import urllib.request
import xml.etree.ElementTree as ET

# contents = 20
# result = 10034

# print(result/contents)
# print(result%contents)
# print(math.ceil(result/contents))


# total = math.ceil(result/contents)

# SAUNA_SEARCH_URL_FORMAT = 'https://sauna-ikitai.com/search?ordering=ikitai_counts_desc&page={0}&prefecture[]=aichi&prefecture[]=akita&prefecture[]=aomori&prefecture[]=chiba&prefecture[]=ehime&prefecture[]=fukui&prefecture[]=fukuoka&prefecture[]=fukushima&prefecture[]=gifu&prefecture[]=gunma&prefecture[]=hiroshima&prefecture[]=hokkaido&prefecture[]=hyogo&prefecture[]=ibaraki&prefecture[]=ishikawa&prefecture[]=iwate&prefecture[]=kagawa&prefecture[]=kagoshima&prefecture[]=kanagawa&prefecture[]=kochi&prefecture[]=kumamoto&prefecture[]=kyoto&prefecture[]=mie&prefecture[]=miyagi&prefecture[]=miyazaki&prefecture[]=nagano&prefecture[]=nagasaki&prefecture[]=nara&prefecture[]=niigata&prefecture[]=oita&prefecture[]=okayama&prefecture[]=okinawa&prefecture[]=osaka&prefecture[]=saga&prefecture[]=saitama&prefecture[]=shiga&prefecture[]=shimane&prefecture[]=shizuoka&prefecture[]=tochigi&prefecture[]=tokushima&prefecture[]=tokyo&prefecture[]=tottori&prefecture[]=toyama&prefecture[]=wakayama&prefecture[]=yamagata&prefecture[]=yamaguchi&prefecture[]=yamanashi'

# print(SAUNA_SEARCH_URL_FORMAT.format(11))

# # for i in range(1, total):
# #   print(i + 1)

# print(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/sauna_data.csv"))



url = 'https://www.geocoding.jp/api/'
params = {
    'q': 'サウナしきじ',
}
url_params = '{}?{}'.format(url, urllib.parse.urlencode(params))
req = urllib.request.Request(url=url_params, method='GET')

geocoding_result = ""

try:
    with urllib.request.urlopen(req) as response:
      geocoding_result = response.read()
    
    root = ET.fromstring(geocoding_result)
    print('\n\n--------------------------------------\n\n')
    print(root)
    
    
    coordinate = root.findall('coordinate')
    
    for co in coordinate:
      print(co.find("lat").text)
      print(co.find("lng").text)
      
    
    print('\n\n--------------------------------------\n\n')

      
except urllib.error.URLError as e:
    print(e.reason)
  
