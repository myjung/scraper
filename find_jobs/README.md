# 로켓펀치 스파이더

### 조회 방식

start url = https://www.rocketpunch.com/jobs
coockie 및 headers 설정함
해당 페이지를 referer로 설정하고

https://www.rocketpunch.com/api/jobs/template?page=1&q=

1페이지에 쿼리를 보냄 (최종 페이지를 뽑기 위해 따로 분류함)

이후 range(2,last_page)를 이용해 전체 페이지를 순회 함
각 페이지 순회시 referer를
https://www.rocketpunch.com/jobs?page={number} 로 설정하고
실제 데이터는
https://www.rocketpunch.com/api/jobs/template?page={number}&q="
로 요청함

Rocketpunch job_detail 스파이더
jobs 스파이더를 통해 산출한 id 를 기준으로 전체 페이지를 조회하여 각 job_detail 정보를 구함
https://www.rocketpunch.com/jobs/{id}/title

    - `f"https://www.rocketpunch.com/jobs/{id}"`
    - 페이지의 경우 하위 페이지로 redirection 발생 status code : 302 하위 경로에 title 데이터를 추가함
    - `f"https://www.rocketpunch.com/jobs/{id}/title"`

### Rocketpunch items를 저장할 db구조

|  TABLES   |
| :-------: |
|   pages   |
| companies |
|   jobs    |

- pages

  - auto increment_key pk
  - 크롤링 시작한 타임스탬프
  - page number
  - job_id fk

- companies

  - company_id pk
  - company_name
  - company_tech_stacks
  - company_description
  - company_products
  - foundation_date
  - 복지
  - member_range
  - assets
  - homepage
  - army_services
  - location
  - industry

- jobs

  - job_id pk
  - company_id fk
  - title
  - work
  - speicalities
  - 분야
  - 지역
  - 경력
  - set(계약, 정규, 인턴) 고용형태
  - smallint 연봉 start
  - smallint 연봉 end
  - date 공고 수정
  - date 공고 마감

- tech_tags
  - tag_id pk
  - varchar tag_name

---

### 로켓펀치 페이지 조회 방법

1. 페이지 > 회사 > 잡 상세 정보의 계층구조
2. 페이지에서 받은 response를 items로 분할하는 슈도코드

```python
item_page = {}
get_page_info(page)
for company in companies:
    company_item = get_company_info(company)
    for job in jobs:
        job_item = get_job_info(job)
        itemp_page.append(job_id)
        yield job_item
    yield company_item
yield item_page
```
