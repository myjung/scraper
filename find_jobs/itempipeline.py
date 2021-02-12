import sqlalchemy

class PrintData:
    def process_item(self, item, spider):
        spider.logger.debug(f"current page is {item['page']}")
        for company in item["company_list"]:
            print(company["company_name"], end="\t")
            print(
                [
                    (job["job_title"], job["job_date_until"])
                    for job in company["job_details"]
                ]
            )
        return f"{item['page']} page printing is finished"


class ProcessToDB:
    def process_item(self, item, spider):
        pass


if __name__=="__main__":
    print(sqlalchemy.__version__)