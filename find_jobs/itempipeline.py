import sqlalchemy
from sqlalchemy import create_engine, text


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
    def open_spider(self, spider):
        spider.logger.info("item pipeline opend")
        self.engine = create_engine(
            "sqlite+pysqlite:///:memory:", echo=True, future=True
        )
        self.conn = self.engine.connect()

    def close_spider(self, spider):
        spider.logger.info("item pipeline closed")

    def process_item(self, item, spider):
        pass


def main():
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
        )
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2}
        )
        for row in result:
            print(f"x: {row.x}  y: {row.y}")
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
        )
        conn.commit()


def main2():
    from sqlalchemy import MetaData
    from sqlalchemy import Table, Column, Integer, String
    from sqlalchemy import ForeignKey

    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

    metadata = MetaData()
    user_table = Table(
        "user_account",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )
    print(type(user_table.c.name))
    print(user_table.c.keys())
    print(user_table.primary_key)

    address_table = Table(
        "address",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user_account.id"), nullable=False),
        Column("email_address", String, nullable=False),
    )

    print(address_table.foreign_keys)

    metadata.create_all(engine)


if __name__ == "__main__":
    print(sqlalchemy.__version__)
    # main2()
