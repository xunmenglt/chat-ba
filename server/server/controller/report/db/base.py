import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker


SQL_URL="mysql+pymysql://root:lt204330@localhost:3306/qiye"

qiye_engine = create_engine(
    SQL_URL,
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),
)

Qiye_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=qiye_engine)

Qiye_Base: DeclarativeMeta = declarative_base()
