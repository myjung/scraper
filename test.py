from sqlalchemy import MetaData, Table, Column, Integer, String, DATE, ForeignKey
import sqlalchemy
from os.path import abspath

db_path = "./temporary_db/sample.db"
db_url = f"sqlite:///{abspath(db_path)}"
engine = sqlalchemy.create_engine(db_url, echo=True, future=True)
meta = MetaData()
scrap = Table(
    "scrap",
    meta,
    Column("job_href", String),
    Column("company_href", String),
    Column("CreatedAt", DATE),
)
job_list = Table(
    "job_list",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("job_id", Integer, ForeignKey("job.id")),
    Column("company_id", Integer, ForeignKey("company.id")),
)
job = Table(
    "job",
    meta,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("stat_info", String),
)
job_specialty = Table(
    "job_specialty",
    meta,
    Column("id", Integer, primary_key=True),
    Column("job_id", Integer, ForeignKey("job.id")),
)
company = Table(
    "company",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("rocketpunch_id", Integer),
    Column("revision", Integer),
    Column("date", DATE),
    Column("href", String),
)
meta.create_all(engine)
