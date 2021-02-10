from scrapy import Spider
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.item import Item, Field
import scrapy


class WantedPage(Item):
    crawled_timedate = Field()
    page_number = Field()


class WantedJob(Item):
    page_address = Field()
    job_id = Field()
    company_id = Field()
    title = Field()
    works = Field()
    speicalities = Field()
    industry = Field()
    location = Field()
    experienced = Field()
    # set(계약, 정규, 인턴) 고용형태
    # smallint 연봉 start
    # smallint 연봉 end
    # date 공고 수정
    # date 공고 마감


class WantedPageSpider(Spider):
    """
    메인 페이지에서 최종 페이지를 구한 후 전체 페이지를 순회한다.
    각 페이지 작업이 끝나면 page, (company...), (job...) 아이템들을 반환한다.
    """

    pass


class WantedJobSpider(Spider):
    """
    데이터 저장소 내의 상세 페이지중 상세 내용을 확인하지 않은 것들을 수집하여 채워 넣는다.
    만약 더 이상 돌 페이지가 없으면 종료
    company, job, tags, techs 등의 아이템을 반환한다.
    """

    pass
