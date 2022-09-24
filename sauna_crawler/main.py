from original_logger import OriginalLogger
from crawler.saunaikitai_crawler import SaunaikitaiCrawler
from crawler.saunaikitai_detail_crawler import SaunaikitaiDetailCrawler
from sauna_crawler.slack.slack_util import SlackUtil
import time
import datetime, os

SLACK_CHANNEL  = os.environ['SLACK_CHANNEL']

slack = SlackUtil()

logger = OriginalLogger()
logger.info("start")
slack.postMessage("サウナイキタイ 解析開始!!", SLACK_CHANNEL)

start_time = time.time()

crawler = SaunaikitaiCrawler()
detail_crawler = SaunaikitaiDetailCrawler()

crawler.crawl()
# detail_crawler.crawl('https://sauna-ikitai.com/saunas/4393')

elapsed_time = datetime.timedelta(seconds=time.time() - start_time)

logger.info("done! {} ".format(str(elapsed_time)))
slack.postMessage("サウナイキタイ 解析終了!! {} ".format(str(elapsed_time)), SLACK_CHANNEL)

