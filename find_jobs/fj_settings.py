from scrapy.settings import Settings


project_settings = {
    'BOT_NAME': 'jrs_bot',
    'DEFAULT_REQUEST_HEADERS': {
        'Accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    },
    'DOWNLOAD_DELAY' : 5,
}

myp = Settings(project_settings)

print(myp)