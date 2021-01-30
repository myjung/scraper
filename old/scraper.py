import requests
import time
import random
from rocketpunch_parser import parse_page, get_last_page_number
from output import all_data

MAIN_URL = "https://www.rocketpunch.com/"

DEFAULT_HEADERS = {
    'authority': 'www.rocketpunch.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'ko-KR,ko;q=0.9',
}

def get_query_params(*args):
    return (('page', args[0]), ('q', ''))


def scrap_pages(end_page = None):
    result = []
    with requests.Session() as session:
        session.headers.update(DEFAULT_HEADERS)  # 메인페이지 접속 시뮬레이션
        main_page = session.get(MAIN_URL)
        session.headers.update({
            'x-csrftoken': main_page.cookies.get('csrftoken'),
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'same-origin',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.rocketpunch.com/jobs',
            'accept-language': 'ko-KR,ko;q=0.9',
        })
        first_response = session.get('https://www.rocketpunch.com/api/jobs/template?page=&q=')
        result.append(parse_page(first_response.content))
        if end_page is None:
            last_page = get_last_page_number(first_response.content)+1
        else:
            last_page = end_page if end_page >= 2 else 2
        # print(f"1페이지 부터 {last_page-1}페이지까지 스크랩 합니다.")
        for page_number in range(2,last_page):
            response = session.get('https://www.rocketpunch.com/api/jobs/template',params=get_query_params(page_number))
            result.append(parse_page(response.content))
            time.sleep(1+(random.random()*5))
    return result




if __name__ == "__main__":
    output = scrap_pages(2)
    # print(output)
    # all_data[0]
    # all_data[-1]
# response = requests.get('https://www.rocketpunch.com/api/jobs/template', headers=headers, params=params)

# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('https://www.rocketpunch.com/api/jobs/template?page=4&q=', headers=headers)
