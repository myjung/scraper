from scrapy import Spider
from scrapy.item import Item, Field
from scrapy.http import Request
import scrapy

from utils import get_ua


class RocketpunchPage(Item):
    page_number = Field()
    companys


class RocketpunchJob(Item):
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


class RocketpunchPageSpider(Spider):
    name = "rocketpunch_jobs"
    hello_url = "https://www.rocketpunch.com/jobs"
    custom_settings = {
        "USER_AGENT" : get_ua(0),
        "DEFAULT_REQUEST_HEADERS":{
        "authority": "www.rocketpunch.com",
        "dnt": "1",
        "accept": "*/*",
        "accept-language": "ko-KR,ko;q=0.9",
        }
    }

    def start_requests():
        """
        Let's say hi to Rocket Punch! If this action succeeds, we can get csrf tokens.
        """
        return [Request(url=hello_url, callback=self.hello_parser)]

    def hello_parser():
        pass

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
