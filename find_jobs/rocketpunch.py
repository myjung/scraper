import scrapy
from scrapy import Spider
from scrapy.crawler import Crawler, CrawlerProcess, CrawlerRunner
from scrapy.http import Request, Response
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from utils import get_ua


class RocketpuchPage(Item):
    """
    페이지 별 회사 리스트 템플릿을 반환하는 아이템
    """

    page = Field()
    company_list = Field()


class RocketpunchPageSpider(Spider):
    """
    first step : https://www.rocketpunch.com/jobs
        response headers를 통해 앞으로 사용할 requests headers를 설정함
    second step : https://www.rocketpunch.com/api/jobs/template?page=&q=
        첫번째 아이템 및 기저조건으로 최종 페이지를 확인 후 한꺼번에 제너레이터를 생성한다.
    second step : https://www.rocketpunch.com/api/jobs/template?page={page_number}&q=
        page_number에 해당하는 이터레이터를 생성하여 전체 페이지에 대해 각각의 아이템을 반환한다. (동시접속 따라 다름)
    """

    name = "rocketpunch_jobs"
    hello_url = "https://www.rocketpunch.com/jobs"
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "USER_AGENT": get_ua(0),  # get first user_agent string
        "DEFAULT_REQUEST_HEADERS": {
            "dnt": "1",  # do not track me
            "accept": "*/*",  # accept all types
            "accept-language": "ko-KR,ko;q=0.9",
        },
        "SCHEDULER_DISK_QUEUE": "scrapy.squeues.PickleFifoDiskQueue",
        "SCHEDULER_MEMORY_QUEUE": "scrapy.squeues.FifoMemoryQueue",
    }

    def start_requests(self):
        """
        Let's say hi to Rocket Punch! If this action succeeds, we can get csrf tokens.
        """
        yield Request(url=self.hello_url, callback=self.hello_parser)

    def parse(self, response):
        pass

    def hello_parser(self, response):
        # print(response.body)
        yield Request(
            url="https://www.rocketpunch.com/api/jobs/template?page=&q=",
            callback=self.first_page_parser,
            meta={"page_number": 1}
        )

    def first_page_parser(self, response):
        data = Selector(text=response.json()["data"]["template"], base_url=response.url)
        end_page_number = int(
            data.css("div.ui.pagination div.disabled.item + a::text").get()
        )
        self.logger.info(end_page_number)
        yield self.page_parser(response)
        for page_number in range(2, 4):
            yield Request(
                url=f"https://www.rocketpunch.com/api/jobs/template?page={page_number}&q=",
                headers={"Referer": "https://www.rocketpunch.com/jobs"},
                callback=self.page_parser,
                meta={"page_number": page_number},
            )

    def page_parser(self, response):
        """
        현재 페이지
        #company-list > div.company             ** 회사의 리스트
        get attr data-company-id                회사 고유 id
            div.content                         -----------------------------
                >div.company-name               -----------------------------
                    >a attr[href]               회사 상세 정보 페이지 주소
                    h4.name::text               회사 이름
                div.description :: text         회사 상세 정보
                div.meta :: text                회사 직무 분야
                div.company-jobs-detail         ** 목록의 리스트
                    a.job-title.link attr[href] 잡 상세 정보 페이지 주소
                    a.job-title.link :: text    잡 이름
                    span.job-stat-info :: text  연봉 및 경력 등
                    >div.job-dates
                        span ~3                 마감일, [기타 근무사항], 수정일

        """
        self.logger.debug("=" * 50)
        self.logger.debug(response.request.headers.to_unicode_dict())
        self.logger.debug(response.meta)
        self.logger.debug("=" * 50)
        text = response.json()["data"]["template"]
        selector = Selector(text=text)

    """
    메인 페이지에서 최종 페이지를 구한 후 전체 페이지를 순회한다.
    각 페이지 작업이 끝나면 page, (company...), (job...) 아이템들을 반환한다.
    """

    """
    first step
    headers = {
    'authority': 'www.rocketpunch.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'x-csrftoken': 'undefined',
    'dnt': '1',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'same-origin',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.rocketpunch.com/jobs',
    'accept-language': 'ko-KR,ko;q=0.9',
    }

    params = (
        ('page', ''),
        ('q', ''),
    )

    response = requests.get('https://www.rocketpunch.com/api/jobs/template', headers=headers, params=params)

    recursive step until end
    headers = {
    'authority': 'www.rocketpunch.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'x-csrftoken': 'undefined',
    'dnt': '1',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'same-origin',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.rocketpunch.com/jobs',
    'accept-language': 'ko-KR,ko;q=0.9',
    }

    params = (
        ('page', '2'),
        ('q', ''),
    )

    response = requests.get('https://www.rocketpunch.com/api/jobs/template', headers=headers, params=params)
    """
    pass


class RocketpunchDetailSpider(Spider):
    """
    데이터 저장소 내의 상세 페이지중 상세 내용을 확인하지 않은 것들을 수집하여 채워 넣는다.
    만약 더 이상 돌 페이지가 없으면 종료
    company, job, tags, techs 등의 아이템을 반환한다.
    """

    pass


def main():
    my_pro = CrawlerProcess()
    my_pro.crawl(RocketpunchPageSpider)
    my_pro.start()


if __name__ == "__main__":
    main()
