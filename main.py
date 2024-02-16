import os
import sentry_sdk

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base
from utils import choices_command
from application import connect


if __name__ == "__main__":

    sentry_sdk.init(
        dsn="https://798a8578ca3d2d3c24f85c54d5afcdac@o4506490164150272.ingest.sentry.io/4506502995247104",
        enable_tracing=True,
    )

    load_dotenv()

    MY_PROTOCOL = os.getenv("PROTOCOL")
    MY_PASSWORD = os.getenv("PASSWORD")
    MY_USERNAME = os.getenv("USERNAME")
    MY_HOST = os.getenv("HOST")
    MY_DATABASE = os.getenv("DATABASE")
    
    engine = create_engine(f"{MY_PROTOCOL}://{MY_USERNAME}:{MY_PASSWORD}@{MY_HOST}/{MY_DATABASE}")
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(bind=engine)

    while True:
        user = connect()
        choices_command(user)
