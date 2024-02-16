from MySQLdb import get_client_info
from sqlalchemy import String, Column, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

from utils import (
    create_contrat_objet,
    create_evenement_objet,
    create_evenement_objet_update,
    get_contrat_signed,
    validate,
    get_contract,
    create_epic_client_objet,
    get_evenement_info,
    get_filter_contrat_signed,
    get_id_contrat,
    post_client_info,
    validate_value_two_date,
    get_name_email,
    create_user_obj,
    get_name_email_collabo,
    validate_prix,
    validate_value_date_contrat,
    val_function_int
)

import sentry_sdk


Base = declarative_base()


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

    @staticmethod
    def get_all(session):
        return session.query(Collaborater).all()

    @staticmethod
    def get_by_name(session, name: str):
        return session.query(Collaborater).get(Collaborater.nom == name)

    @staticmethod
    def create(session):
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

    @staticmethod
    def update(session, value):
        collabo_gestionn = Collaborater(value.nom)
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
            sentry_sdk.capture_message(f"Mise a jour Collaborater : {row}")  # todo
        except Exception as e:
            sentry_sdk.capture_exception(f"Exception, {e}")

    @staticmethod
    def delete(session, value):
        try:
            user = session.query(Collaborater).filter(Collaborater.id == id)
            if not user:
                sentry_sdk.capture_exception(f"Aucun utilisateur")
            for i in user:
                session.delete(i)
                session.commit()
            sentry_sdk.capture_message(f"Delete Collaborater : {user}")
        except Exception as e:
            sentry_sdk.capture_exception(f"Exception, {e}")


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
    
    @staticmethod
    def create(session, value):
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

    def get_by_email(session, email):
        return session.query(Epic_Client).get(Epic_Client.email == email)

    def get_all_client(session):
        return session.query(Epic_Client).all()

    @staticmethod
    def update(value):
        list_fields_one = get_name_email()
        value_list_one = validate_prix(list_fields_one)
        try:
            client_session = (value_list_one["nom"], value_list_one["email"])
            if client_session[0].contact == value.nom:
                list_fields_two = create_epic_client_objet()
                creation, maj_contact = validate_value_two_date("création de l'entreprise ? ", "dernier prise de contact ? ")
                post_client_info(client_session, list_fields_two, creation, maj_contact)
        except Exception as e:
            sentry_sdk.capture_message(e)

    @staticmethod
    def delete(session, value):
        dict_value = get_name_email()

        user = get_client_info(dict_value["nom"], dict_value["email"])

        if not user:
            # print("Le client n'existe pas dans la base de données.")
            return
        for event in get_evenement_info(user[0].id):
            session.delete(event)

        for contrat in get_id_contrat(user[0].id):
            session.delete(contrat)

        for i in user:
            if i.contact == value.nom:
                session.delete(i)
        session.commit()


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
    
    def get_all(session):
        return session.query(Contrat)

    def get_by_id(session, id):
        try:
            return session.query(Contrat).get(Contrat.id == id)
        except Exception as e:
            sentry_sdk.capture_event(e)
    
    @staticmethod
    def create(session):
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

    def get_all(session, signed: bool = True):
        return session.query(Contrat).filter(Contrat.status == signed).all()

    def update(session, value):
        try:
            # Choisis l'id du contrat
            contrat_un = get_id_contrat()
            # Crée la session
            sess_contrat = get_contract(contrat_un)
            
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

    @staticmethod
    def delete(session, id):
        contrat = get_contract(id)
        if contrat is not None:
            evenement_session = session.query(Evenement).filter(
                Evenement.contrat_id == contrat[0].id
            )
            for event in evenement_session:
                session.delete(event)
                session.commit()
            for row in contrat:
                session.delete(row)
                session.commit()


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

    @staticmethod
    def create(session, value):
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

    @staticmethod
    def get_all(session):
        return session.query(Evenement).all()

    @staticmethod
    def get_by_id(session, id: int):
        return session.query(Evenement).get(Evenement.event_id == id)

    @staticmethod
    def update(session, evenement_upgrape):
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

    @staticmethod
    def delete(session, evenement_delete):
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