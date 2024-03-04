import MySQLdb
import bcrypt
from menu import Menu
from menu_factory import create_menu_factory
from models import Collaborator, Contract, EpicClient, Event
from forms import get_id_form, get_create_contract_form, get_create_epic_client_form, get_create_event_form, get_find_collaborator_form, get_find_user_form, get_login_form, get_register_form, get_update_epic_client_form
from state import save, read


def read_only():
    Menu(f"Menu support",
        (               
            ("Consulter les clients",  read_clients),
            ("Consulter les Contracts", read_contracts),
            ("Consulter les évenements",  read_events),
            ("Consuler les contrat no signed",  read_contract_signed),
            ("Retour", print)
        )
    ).run()

def read_contracts():
    contracts = Contract.get_all()
    if not contracts:
        print("Aucun Contract afficher")
    else:
        input("\n".join(str(contract) for contract in contracts))
    

def read_clients():
    clients = EpicClient.get_all()
    input("\n".join(str(client) for client in clients))


def read_contract_signed():
    contracts = Contract.get_no_signed()
    if not contracts:
        print("Aucun Contract afficher")
    else:
        input("\n".join(str(contract) for contract in contracts))


def read_events(no_support: bool = False):
    events = Event.get_all(no_support)
    input("\n".join(str(event) for event in events))


def connect():
    form_data = get_login_form()
    email, password = form_data["email"], form_data["password"]
    collaborator = Collaborator.get_by_email(email)
    if collaborator:
        if bcrypt.checkpw(password.encode("utf-8"), collaborator.password.encode("utf-8")):
            save("current_user", collaborator)
            greetings()
        else:
            print("Le mot de passe est incorrect ! ")
    else:
        print("Email d'utilisateur inconnu ! ")

def greetings():

    current_user = read("current_user")
    
    print(f"Bienvenue {read("current_user").name} !")
    
    if current_user.permission == "gestion":    
        create_menu_factory("GESTIONNAIRE")(
            read_only=read_only,
            create_collaborator=create_collaborator,
            update_collaborator=update_collaborator,
            delete_collaborator=delete_collaborator,
            create_contract_gestion=create_contract_gestion,
            update_contract_gestion=update_contract_gestion,
            update_event=update_event
        ).run()
    elif current_user.permission == "commercial":
        create_menu_factory("COMMERCIAL")(
            read_only=read_only,
            create_client=create_client,
            update_client=update_client,
            delete_client=delete_client,
            update_contract=update_contract,
            create_event=create_event,
            delete_event=delete_event
        ).run()
    elif current_user.permission == "support":
        create_menu_factory("SUPPORT")(
            read_only=read_only
        ).run()


def register():
    form_data = get_register_form()
    try:
        Collaborator.create(**form_data)
    except ValueError as e:
        input(f"Erreur: {e} ")
    except MySQLdb.IntegrityError:
        input(f"Erreur: Email déja utilisée")
    create_menu_factory("PRINCIPAL")(connect, register).run()


def create_collaborator():
    form_data = get_register_form()
    try:
        Collaborator.create(**form_data)
    except ValueError as e:
        input(f"Erreur: {e} ")     
    except MySQLdb.IntegrityError:
        input(f"Erreur: Email déja utilisée") 
    create_menu_factory("GESTIONNAIRE")(connect, register, update_collaborator, delete_collaborator).run()
    

def update_collaborator():
    form_data_email = get_find_collaborator_form()
    try:
        Collaborator.update(**form_data_email)
    except ValueError as e:
        input(f"Erreur: {e} ")  
    except IndexError:
        input(f"Erreur: mauvais email")
    create_menu_factory("GESTIONNAIRE")(connect, register, update_collaborator, delete_collaborator).run()


def delete_collaborator():
    form_data_email = get_find_collaborator_form()
    try:
        Collaborator.delete(**form_data_email)
    except IndexError:
        input(f"Erreur: mauvais email")
    create_menu_factory("GESTIONNAIRE")(connect, register, update_collaborator, delete_collaborator).run()
    
    
def create_client():
    form_data = get_create_epic_client_form()
    try:
        EpicClient.create(contact_id=read("current_user").id, **form_data)
    except MySQLdb.IntegrityError:
        input(f"Erreur: Email déja utilisée")
    create_menu_factory("COMMERCIAL")(read_only, create_client, update_client, delete_client, update_client, delete_client, delete_event).run()


def update_client():
    form_data_email = get_find_user_form()
    try:
        EpicClient.update(**form_data_email)
    except IndexError:
        input("Vous avez taper un identifiant qui n'existe pas")
    except MySQLdb.IntegrityError:
        input(f"Erreur: Email déja utilisée")
    create_menu_factory("COMMERCIAL")(read_only, create_client, update_client, delete_client, update_client, delete_client, delete_event).run()
    
    
def delete_client():
    form_data_email = get_find_user_form()
    try:
        EpicClient.delete(**form_data_email)
    except IndexError:
        input("Vous avez taper un identifiant qui n'existe pas")
    create_menu_factory("COMMERCIAL")(read_only, create_client, update_client, delete_client, update_client, delete_client, delete_event).run()
    
    
def create_contract_gestion():
    form_data = get_create_contract_form()
    Contract.create(contact_id=read("current_user").id, **form_data)
    create_menu_factory("GESTIONNAIRE")(create_collaborator, update_collaborator, delete_collaborator, create_contract_gestion, update_contract_gestion, update_event).run()
    
    
def update_contract_gestion():
    form_data = get_id_form()
    try:
        Contract.update(**form_data)
    except IndexError:
        input("Vous avez taper un identifiant qui n'existe pas")
    create_menu_factory("GESTIONNAIRE")(create_collaborator, update_collaborator, delete_collaborator, create_contract_gestion, update_contract_gestion, update_event).run()
    
    

    
    
def update_contract():
    form_data = get_id_form()
    try:
        Contract.update(**form_data)
    except IndexError:
        input("Vous avez taper un identifiant qui n'existe pas")
    create_menu_factory("COMMERCIAL")(read_only, create_client, update_client, delete_client, update_contract, create_event).run()
  
    
def delete_contract():
    form_data = get_id_form()
    try:
        Contract.delete(**form_data)
    except IndexError:
        input("Vous avez taper un identifiant qui n'existe pas")
    create_menu_factory("COMMERCIAL")(read_only, create_client, update_client, delete_client, update_contract, create_event).run()


def create_event():
    form_data = get_create_event_form()
    try:
        Event.create(**form_data)
    except ValueError:
        input(f"Erreur: mauvais support")
        create_menu_factory("COMMERCIAL")(read_only, create_client, update_client, delete_client, update_contract, create_event, delete_event).run()
    
def update_event():
    form_data = get_id_form()
    try:
        Event.update(**form_data)
    except IndexError:
        input("Vous avez taper un identifiant qui n'existe pas")
    
    
def delete_event():
    form_data = get_id_form()
    try:
        Event.delete(**form_data)
    except IndexError:
        input("Vous avez taper un identifiant qui n'existe pas")
    create_menu_factory("COMMERCIAL")(read_only, create_client, update_client, delete_client, update_contract, create_event, delete_event).run()
