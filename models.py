from models_users import (
    Collaborater,
    choice_menu_user,
    connect,
)
from utils import email_validator, get_choice, str_validator, validate
from utils_obj import create_contrat_objet, create_epic_client_objet, create_evenement_objet, create_evenement_objet_update
from val_function_contrat import validate_prix
from val_function_evenement import (
    validate_value_date_contrat,
    validate_value_two_date,
)
from val_function_string_int import val_function_int
from sqlalchemy import create_engine
from sqlalchemy import String, Column, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
import sentry_sdk

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


class Epic_Client(Base):
    __tablename__ = "epic_client"

    id = Column(Integer, primary_key=True)
    nom = Column(String(30), unique=True, index=True)
    email = Column(String(30), unique=True, index=True)
    telephone = Column(String(30), unique=True, index=True)
    entreprise = Column(String(30))
    creation = Column(DateTime(timezone=True))
    maj_contact = Column(DateTime(timezone=True))
    contact = Column(String(250), ForeignKey(Collaborater.nom))

    def __str__(self) -> str:
        return f"('Le Client D'Epic {self.nom!r}{self.email!r}{self.telephone!r}{self.entreprise!r}{self.creation!r}')"

    def __repr__(self) -> str:
        return f"('Client D'Epic {self.nom!r}{self.email!r}{self.telephone!r}{self.entreprise!r}{self.creation!r}{self.maj_contact!r}{self.contact!r}')"


def get_client_info(nom, email):
    return (
        session.query(Epic_Client)
        .filter(Epic_Client.nom == nom)
        .filter(Epic_Client.email == email)
    ).all()


def get_all_client():
    sess_client = session.query(Epic_Client)
    for row in sess_client:
        print(row)


def get_name_email():
    return [
        {
            "name": "nom",
            "description": "Entrer le nom du client ! ",
            "validators": str_validator,
        },
        {
            "name": "email",
            "description": "Entrer l'email du client ! ",
            "validators": email_validator,
        },
    ]


def post_client_info(value_session, list_field, creation, maj_contact):
    for i in value_session:
        i.nom = (list_field["nom"],)
        i.email = (list_field["email"],)
        i.telephone = (list_field["telephone"],)
        i.entreprise = (list_field["entreprise"],)
        i.creation = (creation,)
        i.maj_contact = (maj_contact,)
        i.contact = (i.contact,)
        session.add(i)
        session.commit()
    sentry_sdk.capture_message(i)


def create_client(value):
    try:
        list_field = create_epic_client_objet()
        creation, maj_contact = validate_value_two_date("création de l'entreprise ? ", "dernier prise de contact ? ")
        epic_client = Epic_Client(
            nom=list_field["nom"],
            email=list_field["email"],
            telephone=list_field["telephone"],
            entreprise=list_field["entreprise"],
            creation=creation,
            maj_contact=maj_contact,
            contact=value.nom,
        )
        session.add(epic_client)
        session.commit()
        sentry_sdk.capture_message(epic_client)
    except Exception as e:
        sentry_sdk.capture_exception(e)


def update_client(value):
    list_fields_one = get_name_email()
    value_list_one = validate(list_fields_one)
    try:
        client_session = get_client_info(value_list_one["nom"], value_list_one["email"])
        if client_session[0].contact == value.nom:
            list_fields_two = create_epic_client_objet()
            creation, maj_contact = validate_value_two_date("création de l'entreprise ? ", "dernier prise de contact ? ")
            post_client_info(client_session, list_fields_two, creation, maj_contact)
    except Exception as e:
        sentry_sdk.capture_message(e)


def delete_client(value):
    dict_value = get_name_email()

    user = get_client_info(dict_value["nom"], dict_value["email"])

    if not user:
        print("Le client n'existe pas dans la base de données.")
        return
    for event in get_evenement_info(user[0].id):
        session.delete(event)

    for contrat in get_id_contrat(user[0].id):
        session.delete(contrat)

    for i in user:
        if i.contact == value.nom:
            session.delete(i)
    session.commit()


def choice_menu_client(value):
        while True:
            choice_menu_client = get_choice("1: create\n2: update\n2 3: delete\n ")
            if choice_menu_client == 1:
                create_client(value)
            elif choice_menu_client == 2:
                update_client(value)
            elif choice_menu_client == 3:
                delete_client(value)
            else:
                break


class Contrat(Base):
    __tablename__ = "contrat_user"

    id = Column(Integer, primary_key=True)
    information_id = Column(Integer, ForeignKey("epic_client.id"), nullable=False)
    contact = Column(
        String(30),
        ForeignKey("epic_client.contact"),
        nullable=False,
    )
    prix = Column(Integer)
    rest_prix = Column(Integer)
    creation = Column(DateTime(timezone=True))
    status = Column(Boolean, default=False)

    def __str__(self) -> str:
        return f"(Contrat {self.information_id!r} {self.contact!r} {self.prix!r} {self.rest_prix!r} {self.creation!r} {self.status!r})"

    def __repr__(self) -> str:
        return f"(le Contrat numéro {self.id }, {self.contact!r}, {self.prix}, {self.rest_prix}, {self.status}, {self.creation})"


def get_all_contrat():
    sess_contrat = session.query(Contrat)
    for row in sess_contrat:
        print(row)


def get_info_contrat(id):
    try:
        contrat = session.query(Contrat).filter(Contrat.id == id)
        return contrat
    except Exception as e:
        sentry_sdk.capture_event(e)


def get_id_contrat():
    return int(input("Quel est le numéro du contrat ? "))


def get_filter_contrat_signed():
    return session.query(Contrat).filter(Contrat.status == True).all()


def get_contrat_signed(rest_prix):
    print(rest_prix, "a")
    if rest_prix == 0:
        status = True
    else:
        status = False
    return status


def create_contrat():
    try:
        first_list = get_name_email()
        values_list = validate(first_list)
        client_session = get_client_info(values_list["nom"], values_list["email"])
        contrat = create_contrat_objet()
        creation = validate_value_date_contrat()
        prix, rest_prix = validate_prix()
        status = get_contrat_signed(rest_prix)
        contrat = Contrat(
            information_id=client_session[0].id,
            contact=client_session[0].contact,
            creation=creation,
            prix=prix,
            rest_prix=rest_prix,
            status=status,
        )
        session.add(contrat)
        session.commit()
        sentry_sdk.capture_message(contrat)
    except Exception as e:
        sentry_sdk.capture_exception(e)


def update_contrat(value):
    try:
        # Choisis l'id du contrat
        contrat_un = get_id_contrat()
        # Crée la session
        sess_contrat = get_info_contrat(contrat_un)
        
        if value.nom != sess_contrat[0].contact:
            return None
        else:
            contrat = create_contrat_objet()
            status = get_contrat_signed(contrat["rest_prix"])
        for i in sess_contrat:
            i.information_id = contrat["information_id"]
            i.contact = contrat["contact"]
            i.prix = contrat["prix"]
            i.rest_prix = contrat["rest_prix"]
            i.creation = contrat["creation"]
            i.status = status
            session.add(i)
            session.commit()
            sentry_sdk.capture_message("Mise a jour", i)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        

def delete_contrat(value):
    id = int(input("Choisissez le contrat que vous souhaitez supprimez "))
    contrat = get_info_contrat(id)
    evenement_session = session.query(Evenement).filter(
        Evenement.contrat_id == contrat[0].id
    )
    for i in evenement_session:
        session.delete(i)
        session.commit()
    for row in contrat:
        session.delete(row)
        session.commit()


def choices_menu_contrat(value):
    if value.permission == "commercial" or "gestion":
        message = "create: 1\nmaj: 2\ndel: 3\n"
        choices = get_choice(message)
        if choices == 1:
            create_contrat()
        elif choices == 2:
            update_contrat(value)
        elif choices == 3:
            delete_contrat(value)
        elif choices == 4:
            create_evenement(value)
        else:
            return value
    else:
        print("Vous n'avez pas acces a ce menu, déconnexion")
        session.rollback()


class Evenement(Base):
    __tablename__ = "evenement_user"

    event_id = Column(Integer, primary_key=True, index=True)
    contrat_id = Column(Integer, ForeignKey("contrat_user.id"), nullable=False)
    client_name = Column(String(30), ForeignKey("epic_client.nom"), nullable=False)
    client_contact = Column(ForeignKey("epic_client.email"), nullable=False)
    event_start = Column(DateTime(timezone=True))
    event_end = Column(DateTime(timezone=True))
    support_contact = Column(String(30), ForeignKey(Collaborater.nom), nullable=False)
    location = Column(String(30))
    attendes = Column(Integer)
    NOTES = Column(String(30))

    def __repr__(self) -> str:
        return f" L'Evenement du {self.client_name},{self.client_contact},{self.event_start},{self.event_end}"


def get_all_evenement():
    sess_evenement = session.query(Evenement)
    for row in sess_evenement:
        print(row)


def get_evenement_info(evenement_identifiant):
    return (
        session.query(Evenement)
        .filter(Evenement.event_id == evenement_identifiant)
        .all()
    )


def create_evenement(value):
    try:
        contrat_sess_signed = get_filter_contrat_signed()
        dict_name_email = get_name_email()
        name_email = validate(dict_name_email)
        epic = get_client_info(name_email["nom"], name_email["email"])
        if epic[0].contact != value.nom or contrat_sess_signed[0].information_id != epic[0].id:
            return
        event_start, event_end = validate_value_two_date("création de l'evenement ? ", "fin de l'évenement ? ")
        values_dict = create_evenement_objet()
        evenement = Evenement(
            contrat_id=contrat_sess_signed[0].id,
            client_name=epic[0].nom,
            client_contact=epic[0].email,
            event_start=event_start,
            event_end=event_end,
            support_contact=value.nom,
            location=values_dict["location"],
            attendes=values_dict["attendes"],
            NOTES=values_dict["NOTES"],
        )
        session.add(evenement)
        session.commit()
        sentry_sdk.capture_message(evenement)
    except Exception as e:
        sentry_sdk.capture_exception(e)


def update_evenement(evenement_upgrape):
    evenement_identifiant = val_function_int(evenement_upgrape)
    evenement_session = get_evenement_info(evenement_identifiant)
    event_start, event_end = validate_value_two_date("création de l'evenement ? ", "fin de l'évenement ? ")
    try:
        evenement_update = create_evenement_objet_update()

        session.add(evenement_session)
        session.commit()
        sentry_sdk.capture_message(evenement_session)
    except Exception as e:
        sentry_sdk.capture_exception(e)


def delete_evenement(evenement_delete):
    evenement_identifiant = val_function_int(evenement_delete)
    try:
        session_evenement = get_evenement_info(evenement_identifiant)
        if not session_evenement:
            sentry_sdk.capture_exception(f"Aucun Evenement")
            return
        for i in session_evenement:
            session.delete(i)
            session.commit()
        sentry_sdk.capture_message(f"Delete Evenement : {i}")
    except Exception as e:
        sentry_sdk.capture_exception(f"Exception, {e}")


def get_all():
    get_all_client()
    get_all_contrat()
    get_all_evenement()


def choice_gestionnaire_menu(value):
    choice = get_choice("1: utilisateur\n2: contrat\n3: delete evenement\n")
    if choice == 1:
        choice_menu_user(value)
    elif choice == 2:
        choices_menu_contrat(value)
    elif choice == 3:
        delete_evenement(value)
    else:
        pass


def choice_commercial_menu(value):
    choice = get_choice("1: client\n2: contrat\n3: Créer évenement\n")
    if choice == 1:
        choice_menu_client(value)
    elif choice == 2:
        choices_menu_contrat(value)
    elif choice == 3:
        create_evenement(value)


def choices_command(value):
    while True:
        if not value.nom:
            return connect()
        if value.permission == "gestion":
            choice_gestionnaire_menu(value)
        if value.permission == "commercial":
            choice_commercial_menu(value)
        else:
            pass


Base.metadata.create_all(bind=engine)


def main():
    user = connect()
    choices_command(user)


if __name__ == "__main__":
    while True:
        main()
