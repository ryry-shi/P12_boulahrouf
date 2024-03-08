import os
import sentry_sdk

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from menu_factory import create_menu_factory
from models import Base
from interface import connect, register
from state import save


if __name__ == "__main__":

    sentry_sdk.init(
        dsn="https://798a8578ca3d2d3c24f85c54d5afcdac@o4506490164150272.ingest.sentry.io/4506502995247104",
        enable_tracing=True,
    )

    load_dotenv()

# Construire la chaîne de connexion à la base de données
    engine = create_engine(f"{os.getenv("PROTOCOL")}://root:{os.getenv("PASSWORD")}@{os.getenv("HOST")}/{os.getenv("DATABASE")}")
    Session = sessionmaker(bind=engine)
    session = Session()

    save("session", session)

    Base.metadata.create_all(bind=engine)

    create_menu_factory("PRINCIPAL")(connect, register).run()
