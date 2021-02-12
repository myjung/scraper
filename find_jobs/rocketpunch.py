import scrapy
from scrapy import Spider
from scrapy.crawler import Crawler, CrawlerProcess, CrawlerRunner
from scrapy.http import Request, Response
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from utils import get_ua


class PrintData:
    def process_item(self, item, spider):
        print("type is ", type(item), item["page"])
        for company in item["company_list"]:
            print(company["company_name"], end="\t")
            print(
                [
                    (job["job_title"], job["job_date_until"])
                    for job in company["job_details"]
                ]
            )
        return item


class RocketpuchPage(Item):
    """
    수집하려는 각 페이지를 나타내는 아이템 페이지 번호와 회사 리스트를 가지고 있다.
    """

    page = Field()
    company_list = Field()


class RocketpunchPageSpider(Spider):
    """
    first step : https://www.rocketpunch.com/jobs
        response headers를 통해 앞으로 사용할 requests headers를 설정함
    second step : https://www.rocketpunch.com/api/jobs/template?page=&q=
        첫번째 페이지에 접속해서 전체 페이지 확인 후 한꺼번에 requests를 생성한다.
    """

    name = "rocketpunch_jobs"
    hello_url = "https://www.rocketpunch.com/jobs"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "USER_AGENT": get_ua(0),  # get first user_agent string
        "DEFAULT_REQUEST_HEADERS": {
            "dnt": "1",  # do not track me
            "accept": "*/*",  # accept all types
            "accept-language": "ko-KR,ko;q=0.9",
        },
        "SCHEDULER_DISK_QUEUE": "scrapy.squeues.PickleFifoDiskQueue",
        "SCHEDULER_MEMORY_QUEUE": "scrapy.squeues.FifoMemoryQueue",
        "ITEM_PIPELINES": {
            "rocketpunch.PrintData": 300,
        },
        "FEEDS": {
            "output.json": {
                "format": "json",
                "indent": 2,
                "encoding": "utf8",
                "fields": None,
            }
        },
    }

    def start_requests(self):
        """
        Let's say hi to Rocket Punch! If this action succeeds, we can get csrf tokens.
        """
        yield Request(url=self.hello_url, callback=self.hello_parser)

    def hello_parser(self, response):
        yield Request(
            url="https://www.rocketpunch.com/api/jobs/template?page=&q=",
            callback=self.first_page_parser,
            meta={"page_number": 1},
        )

    def first_page_parser(self, response):
        data = Selector(text=response.json()["data"]["template"], base_url=response.url)
        end_page_number = int(
            data.css("div.ui.pagination div.disabled.item + a::text").get()
        )
        self.logger.info(f"generating 1 to {end_page_number} pages requests")
        yield self.page_parser(response)
        for page_number in range(2, end_page_number+1):
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
        company_list = []
        for company in selector.css("#company-list > div.company"):
            _company_name = company.css("div.content>div.company-name")[0]
            _a = _company_name.css("a[target='_blank']")[0]
            _job_details = company.css("div.company-jobs-detail>div.job-detail")
            company_id = company.attrib["data-company_id"]
            company_href = _a.attrib["href"]
            company_name = "".join(
                _a.css(".header.name>strong::text,small::text").getall()
            )
            company_description = company.css("div.description::text").get()
            company_meta_info = company.css("div.nowrap.meta::text").get()
            job_details = []
            for job in _job_details:
                job_href = job.css("a.job-title::attr(href)").get()
                job_title = job.css("a.job-title::text").get()
                job_stat_info = job.css("span.job-stat-info::text").get()
                _dates = tuple(
                    filter(
                        lambda x: x != "",
                        [
                            text.strip()
                            for text in job.css("div.job-dates>span::text").getall()
                        ],
                    )
                )
                job_date_until = _dates[0]
                job_date_modified = _dates[-1]
                job_date_etc = _dates[1] if len(_dates) == 3 else ""

                job_details.append(
                    {
                        "job_href": job_href,
                        "job_title": job_title,
                        "job_stat_info": job_stat_info,
                        "job_date_until": job_date_until,
                        "job_date_modified": job_date_modified,
                        "job_date_etc": job_date_etc,
                    }
                )
            company_list.append(
                {
                    "company_id": company_id,
                    "company_href": company_href,
                    "company_name": company_name,
                    "company_description": company_description,
                    "company_meta_info": company_meta_info,
                    "job_details": job_details,
                }
            )

        l = ItemLoader(item=RocketpuchPage(), selector=selector)
        l.add_value("page", response.meta["page_number"])
        l.add_value("company_list", company_list)
        return l.load_item()


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
