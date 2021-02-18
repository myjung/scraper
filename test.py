from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DATE,
    ForeignKey,
    Enum,
    BOOLEAN,
)
import sqlalchemy
from os.path import abspath
import enum

db_path = "./temporary_db/sample.db"
db_url = f"sqlite:///{abspath(db_path)}"
engine = sqlalchemy.create_engine(db_url, echo=True, future=True)
meta = MetaData()


scrap = Table(
    "scrap",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("job_href", String),
    Column("job_id", Integer),
    Column("company_href", String),
    Column("company_origin_id", Integer),
)

date_job = Table(
    "date_job",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("scrap_date", DATE),
    Column("job_id", Integer, ForeignKey("job.id")),
    Column("company_id", Integer, ForeignKey("company.id")),
)

company = Table(
    "company",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("origin_id", Integer),
    Column("revision", Integer),
    Column("name", String),
    Column("href", String),
    Column("description", String),
    Column("products", String),
    Column("industries", String),
    Column("welfare", String),
    Column("foundation_date", DATE),
    Column("employee", Integer),
    Column("invest", Integer),
    Column("homepage", String),
    Column("email", String),
    Column("tel", String),
)

company_tech = Table(
    "company_tech",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("company_id", Integer, ForeignKey("company.id")),
    Column("tag", Integer),
)

company_location = Table(
    "company_location",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("company_id", Integer, ForeignKey("company.id")),
    Column("location", String),
)

job = Table(
    "job",
    meta,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("stat_info", String),
    Column("date_until", DATE),
    Column("date_modified", DATE),
    Column("etc", String),
    Column("task", String),
    Column("detail", String),
    Column("recruit", String),
    Column("location", String),
    Column("position", String),
    Column("remote_work", BOOLEAN),
    Column("new_comer", BOOLEAN),
    Column("work_time", Integer),
    Column("salarary", Integer),
)

job_tech = Table(
    "job_tech",
    meta,
    Column("id", Integer, primary_key=True),
    Column("job_id", Integer, ForeignKey("job.id")),
    Column("tag", Integer),
)

meta.create_all(engine)
