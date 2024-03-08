from datetime import datetime
import bcrypt
from sqlalchemy import (
    String,
    Column,
    Integer,
    DateTime,
    TIMESTAMP,
    ForeignKey,
    Boolean
)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

from state import read
from misc import (
    create_or_update,
    delete
)


Base = declarative_base()


class Collaborator(Base):
    __tablename__ = "collaborator"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), index=True)
    password = Column(String(250))
    email = Column(String(250), unique=True)
    affiliation = Column(Integer)
    permission = Column(String(250))

    def __str__(self) -> str:
        return f"Collaborator: {self.id} | {self.name} | {self.email} | {self.affiliation} | {self.permission}"

    def __repr__(self) -> str:
        return f"Collaborator: {self.id} | {self.name} | {self.email} | {self.affiliation} | {self.permission}"

    @staticmethod
    def get_all():
        return read("session").query(Collaborator).all()

    @staticmethod
    def get_by_email(email: str):
        query = read("session").query(Collaborator).filter_by(email=email)
        return query[0] if query.count() != 0 else None
    
    @property
    def events(self):
        return read("session").query(Event).filter(Event.support_contact == self.name)
    
    @staticmethod
    def get_by_name(name: str):
        return read("session").query(Collaborator).filter_by(name=name)[0]

    @staticmethod
    def get_permission_from_affiliation(affiliation: int) -> str:
        if affiliation > 0 and affiliation < 4:
            return {1: "commercial", 2: "support", 3: "gestion"}[affiliation]
        raise ValueError("Affiliation incorrecte")
        
    @staticmethod
    def create(name: str, email: str, password: str, affiliation: int) -> None:
        if read("current_user") is None or (read("current_user") is not None and read("current_user").permission == "gestion"):
            obj = Collaborator(
                name=name,
                password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
                email=email,
                affiliation=affiliation,
                permission=Collaborator.get_permission_from_affiliation(affiliation),
            )
            create_or_update(obj)
            return obj
        else:
            raise ValueError("Droits insuffisants pour créer un utilisateur")

    @staticmethod
    def update(email: str, update_name: str, update_password: str, update_email: str, update_affiliation: int) -> None:
        obj = Collaborator.get_by_email(email)
        obj.name = update_name
        obj.password = bcrypt.hashpw(update_password.encode('utf-8'), bcrypt.gensalt()),
        obj.email = update_email
        obj.affiliation = update_affiliation
        obj.permission = Collaborator.get_permission_from_affiliation(update_affiliation)
        create_or_update(obj)           
        return obj
            
    @staticmethod
    def delete(email: str) -> None:
        obj = Collaborator.get_by_email(email)
        if not obj:
            print("Aucun utilisateurs avec cette email")
        delete(obj)
        

class EpicClient(Base):
    __tablename__ = "epic_client"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    email = Column(String(30), unique=True)
    phone = Column(String(30), unique=True)
    entreprise = Column(String(30))
    creation_date = Column(DateTime(timezone=True))
    contact_id = Column(Integer, ForeignKey(Collaborator.id))
    last_update = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    @property
    def contact(self):
        return read("session").query(Collaborator).get(id=self.contact_id)

    def __str__(self) -> str:
        return f"EpicClient: {self.id} | {self.name} | {self.email} | {self.phone} | {self.entreprise} | {self.creation_date} | {self.last_update} | {self.contact_id}"

    def __repr__(self) -> str:
        return f"EpicClient: {self.id} | {self.name} | {self.email} | {self.phone} | {self.entreprise} | {self.creation_date} | {self.last_update} | {self.contact_id}"

    @staticmethod
    def create(name: str, email: str, phone: str, entreprise: int, creation_date: DateTime, contact_id: int) -> None:
        obj = EpicClient(
            name=name,
            email=email,
            phone=phone,
            entreprise=entreprise,
            creation_date=creation_date,
            contact_id=contact_id
        )
        create_or_update(obj)
        return obj

    @staticmethod
    def get_by_email(email: str):
        return read("session").query(EpicClient).filter_by(email=email)[0]

    def get_all():
        return read("session").query(EpicClient).all()
    
    @staticmethod
    def get_by_id(id: str):
        return read("session").query(EpicClient).filter_by(id=id)[0]

    @staticmethod
    def update(email: str, updated_name: str, updated_email: str, updated_phone: str, updated_entreprise: str) -> None:
        obj = EpicClient.get_by_email(email)
        if obj.contact_id == read("current_user").id and read("current_user").permission == "commercial":
            obj.name = updated_name
            obj.email = updated_email
            obj.phone = updated_phone
            obj.entreprise = updated_entreprise
            create_or_update(obj)
            return obj
        else:
            print("Ce n'est pas votre client ou vous n'avez pas la permission requise")
            
    @staticmethod
    def delete(email: str) -> None:
        obj = EpicClient.get_by_email(email)
        if obj.contact_id == read("current_user").id:
            create_or_update(obj)


class Contract(Base):
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True)
    epic_client = Column(Integer, ForeignKey(EpicClient.id), nullable=False)
    contact_id = Column(Integer, ForeignKey(Collaborator.id), nullable=False)
    amount = Column(Integer)
    remaining_amount = Column(Integer)
    creation_date = Column(DateTime(timezone=True))
    is_signed = Column(Boolean, default=False)

    @property
    def contact(self):
        return read("session").query(Collaborator).get(id=self.contact_id)

    def __str__(self) -> str:
        return f"Contract: {self.id} | {self.epic_client} | {self.contact_id} | {self.amount} | {self.remaining_amount} | {self.creation_date} | {self.is_signed}"

    def __repr__(self) -> str:
        return f"Contract: {self.id} | {self.epic_client} | {self.contact_id} | {self.amount} | {self.remaining_amount} | {self.creation_date} | {self.is_signed}"
    
    @staticmethod
    def get_by_id(id: str):
        return read("session").query(Contract).filter_by(id=id)[0]

    def get_all():
        return read("session").query(Contract).all()

    def get_no_signed():
        return read("session").query(Contract).filter(Contract.is_signed is False)

    @staticmethod
    def get_signed(value: int) -> str:
        return value == 0
    
    @staticmethod
    def create(epic_client: EpicClient,
               contact_id: int, amount: int, remaining_amount: int,
               creation_date: DateTime) -> None:
        obj = Contract(
            epic_client = epic_client,
            contact_id = contact_id,
            amount = amount,
            remaining_amount = remaining_amount,
            creation_date = creation_date,
            is_signed = Contract.get_signed(remaining_amount)
        )
        create_or_update(obj)
        return obj
    
    @staticmethod
    def update(id: int, update_epic_client: int, update_amount: int, update_remaing_amount: int, update_is_signed: bool) -> None:
        obj = Contract.get_by_id(id)
        if read("current_user").permission == "gestion" or \
                (read("current_user").permission == "commercial" and obj.contact_id == read("current_user").id):
            obj.epic_client = update_epic_client
            obj.amount = update_amount
            obj.remaining_amount = update_remaing_amount
            obj.is_signed = Contract.get_signed(update_is_signed)
            create_or_update(obj)
        else:
            raise ValueError("Vous n'avez pas le droit de modifier ce contrat")
        
    @staticmethod
    def delete(id: int) -> None:
        delete(Contract.get_by_id(id))
    

class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey(Contract.id), nullable=False)
    client_name = Column(String(250), ForeignKey(EpicClient.name), nullable=False)
    client_email = Column(String(250), ForeignKey(EpicClient.email), nullable=False)
    event_start = Column(DateTime(timezone=True))
    event_end = Column(DateTime(timezone=True))
    support_contact = Column(String(30), ForeignKey(Collaborator.name), nullable=True)
    location = Column(String(30))
    attendes = Column(Integer)
    notes = Column(String(30))
    
    def __str__(self) -> str:
        return f"Event: {self.id} | {self.client_name} | {self.support_contact} | {self.event_start} | {self.event_end}"
    
    def __repr__(self) -> str:
        return f"Event: {self.id} | {self.client_name} | {self.support_contact} | {self.event_start} | {self.event_end}"

    @staticmethod
    def get_by_id(id: Integer):
        return read("session").query(Event).filter_by(id=id)[0]

    def get_all(no_support: bool = False):
        return read("session").query(Event).filter(Event.support_contact != None) if no_support else read("session").query(Event).all() 
    
    @staticmethod
    def create(contract_id: Contract,
               event_start: DateTime, event_end: DateTime, 
               location: String, attendes: int, notes: int) -> None:
        contract = Contract.get_by_id(contract_id)
        epic_client = EpicClient.get_by_id(contract.epic_client)
        if contract.is_signed is not True:
            raise ValueError("Contrat non signé")
        obj = Event(
            contract_id = contract_id,
            client_name = epic_client.name,
            client_email = epic_client.email,
            event_start = event_start,
            event_end = event_end,
            location = location,
            attendes = attendes,
            notes = notes
        )
        create_or_update(obj)
        return obj
          
    @staticmethod
    def update(id: int, contract_id: int, client_name: str, client_email: str,
               event_end: datetime, support_contact: str, location: str, attendes: int, notes: str) -> None:
        obj = Event.get_by_id(id)
        if obj and (read("current_user").permission == "gestion" or read("current_user").name == obj.support_contact):
            obj.contract_id = contract_id
            obj.client_name = client_name
            obj.client_email = client_email
            obj.event_end = event_end
            obj.support_contact = support_contact
            obj.location = location
            obj.attendes = attendes
            obj.notes = notes
            create_or_update(obj)
        else:
            raise ValueError("Impossible de mettre à jour l'évènement")

    @staticmethod
    def assign_support(id: int, support_contact: str) -> None:
        obj = Event.get_by_id(id)
        if obj and (read("current_user").permission == "gestion" or read("current_user").name == obj.support_contact):
            obj.support_contact = support_contact
            create_or_update(obj)
        else:
            raise ValueError("Impossible d'assigner le membre de l'équipe de support à l'évènement")

    @staticmethod
    def delete(id):
        delete(Event.get_by_id(id))
