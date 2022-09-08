from original_logger import OriginalLogger
from crawler.saunaikitai_crawler import SaunaikitaiCrawler
from crawler.saunaikitai_detail_crawler import SaunaikitaiDetailCrawler
import time

logger = OriginalLogger()
logger.info("start")

start_time = time.time()

crawler = SaunaikitaiCrawler()
detail_crawler = SaunaikitaiDetailCrawler()

# crawler.crawl()
detail_crawler.crawl('https://sauna-ikitai.com/saunas/4393')

elapsed_time = time.time() - start_time

logger.info("done! {} sec".format(elapsed_time))

