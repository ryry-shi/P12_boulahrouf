import bcrypt
from sqlalchemy import String, Column, Boolean, DateTime, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from forms import get_register_form, get_update_contract_form, get_update_epic_client_form, get_update_event_form
from state import read
from misc import create_or_update, delete


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
        return f"{self.name} | {self.email} | {self.affiliation} | {self.permission}"

    def __repr__(self) -> str:
        return f"{self.name} | {self.email} | {self.affiliation} | {self.permission}"

    @staticmethod
    def get_all():
        return read("session").query(Collaborator).all()

    @staticmethod
    def get_by_email(email: str):
        return read("session").query(Collaborator).filter_by(email=email)[0]
    
    
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
        obj = Collaborator(
            name=name,
            password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
            email=email,
            affiliation=affiliation,
            permission=Collaborator.get_permission_from_affiliation(affiliation),
        )
        create_or_update(obj)
        

    @staticmethod
    def update(email: str) -> None:
        obj = Collaborator.get_by_email(email)
        if not obj or read("current_user").affiliation != 3:
            print("Aucun utilisateurs avec cette email")
        form_data = get_register_form()
        obj.name = form_data["name"]
        obj.password = form_data["password"]
        obj.email = form_data["email"]
        obj.affiliation = form_data["affiliation"]
        obj.permission = Collaborator.get_permission_from_affiliation(form_data["affiliation"])
        read("session").add(obj)
        read("session").commit()            
            
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
        return f"{self.name} | {self.email} | {self.phone} | {self.entreprise} | {self.creation_date} | {self.last_update} | {self.contact_id}"

    def __repr__(self) -> str:
        return f"{self.name} | {self.email} | {self.phone} | {self.entreprise} | {self.creation_date} | {self.last_update} | {self.contact_id}"

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

    @staticmethod
    def get_by_email(email: str):
        return read("session").query(EpicClient).filter_by(email=email)[0]

    def get_all():
        return read("session").query(EpicClient).all()
    
    @staticmethod
    def get_by_id(id: str):
        return read("session").query(EpicClient).filter_by(id=id)[0]


    @staticmethod
    def update(email: str) -> None:
        obj = EpicClient.get_by_email(email)
        if obj.contact_id == read("current_user").id:
            form_date = get_update_epic_client_form()
            obj.name = form_date["name"]
            obj.email = form_date["email"]
            obj.phone = form_date["phone"]
            obj.entreprise = form_date["entreprise"]
            create_or_update(obj)
        else:
            print("Ce n'est pas votre client")
            
            
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
        return f"{self.epic_client} | {self.contact_id} | {self.amount} | {self.remaining_amount} | {self.creation_date} | {self.is_signed}"

    def __repr__(self) -> str:
        return f"{self.epic_client} | {self.contact_id} | {self.amount} | {self.remaining_amount} | {self.creation_date} | {self.is_signed}"
    
    @staticmethod
    def get_by_id(id: str):
        return read("session").query(Contract).filter_by(id=id)[0]

    def get_all():
        return read("session").query(Contract).all()

    def get_no_signed():
        return read("session").query(Contract).filter(Contract.is_signed == False)

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
    
    
    @staticmethod
    def update(id: int) -> None:
        obj = Contract.get_by_id(id)
        epic_client = EpicClient.get_by_id(obj.epic_client)
        if epic_client.contact_id == read("current_user").id or read("current_user").permission == "gestion":
            form_data = get_update_contract_form()
            obj.epic_client = form_data["epic_client"]
            obj.amount = form_data["amount"]
            obj.remaining_amount = form_data["remaining_amount"]
            obj.is_signed = Contract.get_signed(form_data["remaining_amount"])
            create_or_update(obj)
        

    @staticmethod
    def delete(id: int) -> None:
        delete(Contract.get_by_id(id))
        

class Event(Base):
    __tablename__ = "evenement_user"

    id = Column(Integer, primary_key=True)
    contrat_id = Column(Integer, ForeignKey(Contract.id), nullable=False)
    client_name = Column(String(30), ForeignKey(EpicClient.name), nullable=False)
    client_email = Column(ForeignKey(EpicClient.email), nullable=False)
    event_start = Column(DateTime(timezone=True))
    event_end = Column(DateTime(timezone=True))
    support_contact = Column(String(30), ForeignKey(Collaborator.name), nullable=True)
    location = Column(String(30))
    attendes = Column(Integer)
    notes = Column(String(30))
    

    def __repr__(self) -> str:
        return f" L'Evenement du {self.client_name},{self.support_contact},{self.event_start},{self.event_end}"


    @staticmethod
    def get_by_id(id: Integer):
        return read("session").query(Event).filter_by(id=id)[0]


    def get_all(no_support: bool = False):
        return read("session").query(Event).filter(Event.support_contact != None) if no_support else read("session").query(Event).all() 


    def get_support_contact(name):
        obj = Collaborator.get_by_name(name)
        if obj.permission == "support":
            return name
        raise ValueError("Mauvais support(Collaborateur avec role: support)")
    
    
    @staticmethod
    def create(contrat_id: Contract,
               event_start: DateTime, event_end: DateTime, 
               location: String, attendes: int, notes: int,
               support_contact: Collaborator = None) -> None:
        contract = Contract.get_by_id(contrat_id)
        epic_client = EpicClient.get_by_id(contract.epic_client)
        if contract.is_signed != True:
            return
        obj = Event(
            contrat_id = contrat_id,
            client_name = epic_client.name,
            client_email = epic_client.email,
            event_start = event_start,
            event_end = event_end,
            location = location,
            attendes = attendes,
            notes = notes,
            support_contact = Event.get_support_contact(support_contact)
        )
        create_or_update(obj)
          
    @staticmethod
    def update(id: int) -> None:
        obj = Event.get_by_id(id)
        if not obj:
            return
        if read("current_user").permission == "gestion" or read("current_user").name == obj.support_contact:
            form_data = get_update_event_form()
            obj.contrat_id = form_data["contrat_id"]
            obj.client_name = form_data["client_name"]
            obj.client_email = form_data["client_email"]
            obj.event_start = form_data["event_start"]
            obj.event_end = form_data["event_end"]
            obj.support_contact = form_data["support_contact"]
            obj.location = form_data["location"]
            obj.attendes = form_data["attendes"]
            obj.notes = form_data["notes"]
            create_or_update(obj)   


    @staticmethod
    def delete(id):
        delete(Event.get_by_id(id))
