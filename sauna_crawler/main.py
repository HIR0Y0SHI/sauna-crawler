from original_logger import OriginalLogger
from crawler.saunaikitai_crawler import SaunaikitaiCrawler
from crawler.saunaikitai_detail_crawler import SaunaikitaiDetailCrawler

logger = OriginalLogger()
logger.info("start")

crawler = SaunaikitaiCrawler()
detail_crawler = SaunaikitaiDetailCrawler()

crawler.crawl()
# detail_crawler.crawl('https://sauna-ikitai.com/saunas/4393')


logger.info("done!")