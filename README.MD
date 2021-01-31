# 프로젝트 설명
 개발자 취업시장의 현황을 파악하기 위해 기술 스택 및 회사 정보를 수집하는 프로젝트입니다.
 - 한달에 한 번 전체 구직 정보를 수집하여 데이터 저장소에 보관
 - 해당 데이터 저장소에서 통계자료를 생성함
 - 생성한 통계자료를 API를 통해 제공
 - 수집 대상 정보
    - 구인 사이트의 포지션별 채용 현황
    - 포지션 별 필요한 기술 스택
    - 필터링을 위한 복지정보, 회사 위치, 규모 등

# Rocketpunch
 1. https://www.rocketpunch.com/robots.txt 를 통해 확인한 결과 2021/01/30 현재 /jobs/{number}/{title} 와 /companies/{title} 정보는 접근이 가능함 delay time제한이 명시되어 있지 않으므로 인터벌은 짧게 주고 agent 하나를 이용하여 수집함
 2. 수집 방식의 경우 해당 시점에서 https://media.rocketpunch.com/rocketpunch-sitemap/sitemap-job-1.xml.gz 을 이용하여 갱신되어 있는 구인 게시글 주소들을 전부 수집함
    - 갱신 주기 확인 필요 
    - 1/30에 1/27까지 갱신되어 있음
 3. 위에서 추가한 잡 주소들을 순회하며 상세 페이지를 파싱
 4. 기업 상세정보 확인을 위해 3에서 파싱된 데이터를 이용해서 기업 상세정보를 검색함, 기업 상세정보가 없을 경우 이미 마감된 구인이므로 제거함
 5. 구인 정보를 데이터 저장소에 보내고 기업 상세정보를 중복확인 후 데이터 저장소에 추가함
 6. 작성시점에서 3500개 가량의 구인글이 올라와 있음
 * 필드 없는 경우에 대해 대비해야함

## 로켓펀치 데이터 수집 순서
1. 로켓펀치 api 경로 이용할 경우 각 페이지 별로 https://www.rocketpunch.com/jobs?page={number} 를 통해 다음과 같은 데이터가 반환됨 
   - 평균적으로 15kb 정도의 용량

 ```javascript
 response ={
    meta: {code : 200},
    data: {
       template : JSON.stringify(HTML) ,
       title : "채용 정보 | 로켓펀치 - 비즈니스 네트워크" 
       seou_url : "https://www.rocketpunch.com/jobs",
    }
 }
 ```

2. response template 구조
   - css('div#company-list')로 최상단 래퍼를 확인 할 수 있음
   - css('div.company.item')로 각 회사별 정보를 나눠서 확인할 수 있음
   - 위에서 얻은 노드들은 attribute data-company_id를 통해 회사 고유 id를 얻을 수 있음 
   - div.content div.company-name 으로 회사 이름과 상세 접속 페이지를 얻을 수 있음
   - 'div.company-name>a:first-of-type' css 셀렉터로 회사 이름을 확인할 수 있음 하위에 span으로 회사이름 텍스트가 존재함
   - div.company-jobs-detail 로 잡 상세 정보를 구할 수 있음

## - modified
- ~~robots.txt 준수를 위해 https://rocketpunch.com/api 경로를 사용하던 스크래퍼는 폐기함~~
- ~~sitemap을 이용하여 수집하는 비용을 줄임~~
- sitemap 갱신이 너무 늦어 api경로를 사용하는 방식으로 변경함
- 향후 문제제기가 있을 경우 splash를 통해 ajax 로딩을 직접 하는 방식으로 변경

```
- 로켓펀치 협업문의에 공식적으로 크롤링해도 되는지 문의 했으나 (21년 01월 23일) 답장이 없어 그냥 robots.txt 준수하면서 크롤링 하기로 결정함
- 원티드는 협조요청할 깜냥이 없어 그냥 둘 다 동일한 기준으로 진행
```

# Wanted
 1. https://www.wanted.co.kr/robots.txt 를 통해 확인한 결과 현재 개인정보를 제외하고 구인 상세 정보와, 회사정보는 수집이 가능함
 2. https://www.wanted.co.kr/sitemap_kr_company_beta_1.xml 경로를 이용해 기업 정보 상세 페이지 전체 리스트를 확인할 수 있음 갱신 주기는 하루 정도 되는 듯
 3. jobs 페이지의 경우 sitemap 제공이 안되므로 검색 페이지 전체를 수집하여 순회하는 방식으로 진행해야 함, 단 무한스크롤 방식이므로 검색이 수월함
 4. https://www.wanted.co.kr/api/v4/jobs?country=all&job_sort=job.latest_order&locations=all&years=-1&limit={100}&offset={0} limit와 offset 수치를 조절해서 순차 검색이 가능함
 5. response에서 response.link.next가 null이면 연결리스트가 끝났으므로 탐색 종료
 6. request header에 토큰 없어도 조회가능
 7. json을 반환하므로 파싱 난이도가 낮음 현재 api 버전은 4
 8. 작성시점에서 7000개 가량의 구인 글이 올라와 있음

# etc.
 1. jobpanet, saramin, incruit 등은 개발자 구인글이 부족해보여서 두 사이트로 한정함

# 프로젝트 진행 계획
 1. 로켓펀치에서 동작하는 스크래퍼 구현
    - rocketpunch에서 사이트맵을 불러와 대상 url을 선택하기
    - 사이트맵에서 선택된 urls에 대해 순차적으로 데이터를 읽어오기
 2. 원티드에서 동작하는 스크래퍼 구현
    - /api/v4/jobs 에서 전체 데이터를 수집
    - 전체 데이터에서 개별 url을 순회하며 상세 데이터 수집
 3. 스크래퍼에서 모은 데이터를 처리하는 파이프라인 구현
    - raw데이터와 파싱 데이터 둘다 보관함 
    - 데이터 용량이 크지 않고 수집 주기가 길어 일반 로컬파일로 보관해도 문제 없음
    - 향후에는 성능 향상 및 공부 목적으로 적합한 data warehouse 사용하여 보관
    - 중복된 데이터는 고려X
    - 각 시기별로 state를 확인하는 통계이므로 모든 데이터를 수집함
 4. 프론트엔드에서 다른 사용자들이 결과를 확인할 수 있도록 데이터를 제공하는 API 구현
    - 우선 동일 프로젝트 내에서 하위폴더에 api를 구현
    - 무료 인스턴스 또는 serverless 이용해 배포하고 리포지토리 분리
 5. 스크래핑 진행 상황 및 모니터링 할 수 있는 대시보드 구현
    - 누락된 데이터, 사용현황 등 각종 로그 수집할 경로 필요
 6. 로켓펀치와 원티드 구인정보를 종합하여 한번에 현황 파악하기
    - 각 사이트 별로 구인 및 회사의 고유 id를 생성할 수단 찾기
    - 실패할 경우 유사도를 측정하여 동일하게 처리할 수 있는 로직 만들기
    - 또 실패할 경우 그냥 스프레드시트 이용해서 분류하기 7000개 정도라 가능은 함