import json
from bs4 import BeautifulSoup

def get_last_page_number(json_data):
    try:
        json_dict = json.loads(json_data)
    except TypeError:
        json_dict = json.load(json_data)
    soup = BeautifulSoup(json_dict['data']['template'], "lxml")
    last_page = int(soup.select_one('div.ui.pagination div.disabled.item + a').text)
    return last_page


def parse_job_detail(job):
    result = {}
    job_link = getattr(job, 'a', None)
    job_title = getattr(job_link, 'text', None)
    job_href = job_link['href'] if job_link.has_attr('href') else None
    job_stat = getattr(job.span, 'text', None)
    result['job_title'] = job_title
    result['job_href'] = job_href
    result['job_stat'] = job_stat
    return result


def parse_company(company):
    name = company.select_one('div.company-name')
    company_detail_link = getattr(name, 'a', None)
    company_info = company_detail_link['href'] if company_detail_link.has_attr('href') else ''
    description = company.select_one('div.description')
    meta = company.select_one('div.meta')
    applicant = company.select_one('div.applicants')
    jobs = company.select('div.job-detail')  # list
    detail_jobs = []
    for job in jobs:
        detail_jobs.append(parse_job_detail(job))
    return {
        "name": safe_text(name),
        "company_href": company_info,
        "description": safe_text(description),
        "meta": safe_text(meta),
        "current_applicant": safe_text(applicant),
        "job_details": detail_jobs
    }


def safe_text(tag):
    if tag is not None:
        return tag.text
    else:
        return None

def parse_page(json_data):
    try:
        json_dict = json.loads(json_data)
    except TypeError:
        json_dict = json.load(json_data)
    
        
    soup = BeautifulSoup(json_dict['data']['template'], "lxml")
    companies = soup.select('div#company-list div.content')
    result = []
    for company in companies:
        try:
            result.append(parse_company(company))
        except Exception as E:
            print(E)
    return result


if __name__ == '__main__':
    with open("sample_data.json") as f:
        result = parse_page(f)
        print(result)
