from sqlalchemy import create_engine
from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from utils import email_validator, get_choice, str_validator, validate
import bcrypt
import sentry_sdk
import os

from utils_obj import create_user_obj

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

Base = declarative_base()

engine = create_engine(
    f"{MY_PROTOCOL}://{MY_USERNAME}:{MY_PASSWORD}@{MY_HOST}/{MY_DATABASE}"
)
Session = sessionmaker(bind=engine)
session = Session()


class Collaborater(Base):
    __tablename__ = "collaborater"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(250), index=True)
    password = Column(String(250), index=True)
    email = Column("email_address", String(250), index=True)
    affiliation = Column(Integer)
    permission = Column(String(250), index=True)

    def __str__(self) -> str:
        return f" Bonjour {self.nom!r}, {self.email},{self.affiliation}, {self.permission})"

    def __repr__(self) -> str:
        return f" Bonjour {self.nom!r}, {self.email},{self.affiliation}, {self.permission})"


def get_all_user():
    return session.query(Collaborater).all()


def get_user_info(nom):
    session_user = session.query(Collaborater).filter(Collaborater.nom == nom).all()
    if not session_user:
        return None
    return session_user

def get_name_email_collabo():
    return [
        {
            "name": "nom",
            "description": "le nom du collabo",
            "validators": str_validator,
        },
        {
            "name": "email",
            "description": "email du collabo",
            "validators": email_validator,
        },
    ]


def create_user():
    user_values, affiliation, permission = create_user_obj()
    try:
        user = Collaborater(
            nom=user_values["nom"],
            password=user_values["password"],
            email=user_values["email"],
            affiliation=affiliation,
            permission=permission,
        )
        session.add(user)
        session.commit()
        sentry_sdk.capture_message(f"Collaborater créé : {user}")
    except Exception as e:
        sentry_sdk.capture_exception(f"Exception, {e}")


def update_user(value):
    collabo_gestionn = get_user_info(value.nom)
    try:
        if collabo_gestionn[0].permission == "gestion":
            list_fields = get_name_email_collabo()
            values_dict = validate(list_fields)
            collabo_session = (
                session.query(Collaborater)
                .filter(Collaborater.nom == values_dict["nom"])
                .filter(Collaborater.email == values_dict["email"])
            )
            user_values, affiliation, permission = create_user_obj()
            for row in collabo_session:
                row.nom = user_values["nom"]
                row.password = user_values["password"]
                row.email = user_values["email"]
                row.affiliation = affiliation
                row.permission = permission
                session.add(row)
                session.commit()
        sentry_sdk.capture_message(f"Mise a jour Collaborater : {user}")
    except Exception as e:
        sentry_sdk.capture_exception(f"Exception, {e}")


def delete_user(value):
    try:
        id = input("Choissisez le nom du collaborater a delete ! ")
        user = session.query(Collaborater).filter(Collaborater.id == id)
        if not user:
            sentry_sdk.capture_exception(f"Aucun utilisateur")
        for i in user:
            session.delete(i)
            session.commit()
        sentry_sdk.capture_message(f"Delete Collaborater : {user}")
    except Exception as e:
        sentry_sdk.capture_exception(f"Exception, {e}")


def choice_menu_user(value):
    while True:
        choice_menu_client = get_choice("1: créer\n2: update\n3: delete\n")
        if choice_menu_client == 1:
            create_user()
        elif choice_menu_client == 2:
            update_user(value)
        elif choice_menu_client == 3:
            delete_user(value)


def connect():
    inp = input("Si vous n'avez pas de compte appuyez 1 !")
    if inp == str(1):
        return create_user()
    nom = input("Votre nom : ")
    password = input("Votre password : ")
    users = get_user_info(nom)
    if not users:
        print("Aucun utilisateurs trouver ! ")
        return connect()
    mdp = users[0].password
    mdp_boolean = bcrypt.checkpw(
        password=password.encode("utf-8"), hashed_password=mdp.encode("utf-8")
    )
    if mdp_boolean is True:
        user_session = get_user_info(nom)
        for i in user_session:
            print(f"Bonjour {i.nom} {i.email} {i.affiliation}")
        return i
    elif mdp_boolean is False:
        print("Erreur, le mot de passe ou le nom est incorecct ! ")
        return connect


Base.metadata.create_all(bind=engine)

user = session.query(Collaborater)
