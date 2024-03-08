import MySQLdb
import bcrypt
import sentry_sdk

from menu_factory import create_menu_factory
from models import (
    Collaborator,
    Contract,
    EpicClient,
    Event
)
from forms import (
    get_create_collaborator_form,
    get_id_form,
    get_create_contract_form,
    get_create_epic_client_form,
    get_create_event_form,
    get_find_collaborator_form,
    get_find_user_form,
    get_login_form,
    get_register_form,
    get_update_epic_client_form,
    get_assign_support_event_form
)
from state import (
    save,
    read
)
from utils import print_error


def show_menu_gestionnaire():
    """ Affiche un menu gestionnaire """
    return create_menu_factory("GESTION")(
        disconnect=disconnect,
        read_only=read_only,
        create_collaborator=create_collaborator,
        update_collaborator=update_collaborator,
        delete_collaborator=delete_collaborator,
        create_contract_gestion=create_contract_gestion,
        update_contract_gestion=update_contract_gestion,
        assign_support_event=assign_support_event
    ).run()


def show_menu_commercial():
    """ Affiche un menu commercial """
    return create_menu_factory("COMMERCIAL")(
        disconnect=disconnect,
        read_only=read_only,
        create_client=create_client,
        update_client=update_client,
        delete_client=delete_client,
        update_contract=update_contract,
        create_event=create_event,
        delete_event=delete_event,
        read_non_signed_contracts=read_non_signed_contracts
    ).run()


def show_menu_support():
    """ Affiche un menu support """
    return create_menu_factory("SUPPORT")(
        disconnect=disconnect,
        read_only=read_only,
        update_event=update_event,
        read_support_events=read_support_events
    ).run()


def show_menu_principal():
    """ Affiche un menu principal """
    create_menu_factory("PRINCIPAL")(
        connect=connect,
        register=register
    ).run()


def show_menu_consulter():
    """ Affiche un menu consulter """
    create_menu_factory("CONSULTER")(
        read_clients=read_clients,
        read_contracts=read_contracts,
        read_events=read_events
    ).run()


def read_only():
    """ Permet de consulter les données en lecture seule """
    permission = read("current_user").permission.upper()
    show_menu_consulter()
    if permission == "GESTION":
        show_menu_gestionnaire()
    elif permission == "COMMERCIAL":
        show_menu_commercial()
    elif permission == "SUPPORT":
        show_menu_support()


def read_contracts():
    """ Permet de consulter les contrats """
    contracts = Contract.get_all()
    if not contracts:
        print("Aucun Contract afficher")
    else:
        input("\n".join(str(contract) for contract in contracts))


def read_support_events():
    """ Permet de consulter les evenements associés à un collaborateur support """
    events = read("current_user").events
    if not events:
        print("Aucun évènement à afficher")
    else:
        input("\n".join(str(event) for event in events) + "\n")
    show_menu_support()


def read_clients():
    """ Permet de consulter les clients """
    clients = EpicClient.get_all()
    if not clients:
        print("Aucun client à afficher")
    else:
        input("\n".join(str(client) for client in clients) + "\n")


def read_events(no_support: bool = False):
    """ Permet de consulter les évènements """
    events = Event.get_all(no_support)
    if not events:
        print("Aucun évènement à afficher")
    else:
        input("\n".join(str(event) for event in events) + "\n")


def read_non_signed_contracts():
    """ Permet de consulter les contrats non signés """
    contracts = Contract.get_no_signed()
    if not contracts:
        print("Aucun contrat à afficher")
    else:
        input("\n".join(str(contract) for contract in contracts) + "\n")
    show_menu_commercial()


def connect():
    """ Permet de se connecter en tant que collaborateur """
    form_data = get_login_form()
    email, password = form_data["email"], form_data["password"]
    collaborator = Collaborator.get_by_email(email)
    if collaborator:
        if bcrypt.checkpw(password.encode("utf-8"), collaborator.password.encode("utf-8")):
            save("current_user", collaborator)
            greetings()
        else:
            print_error("Le mot de passe est incorrect ! ")
            show_menu_principal()
    else:
        print_error("L'utilisateur est inconnu ! ")
        show_menu_principal()


def greetings():
    """ Permet d'accueillir le collaborateur authentifié """
    current_user = read("current_user")

    print(f"Bienvenue {read("current_user").name} !")
    
    if current_user.permission == "gestion":    
        show_menu_gestionnaire()
    elif current_user.permission == "commercial":
        show_menu_commercial()
    elif current_user.permission == "support":
        show_menu_support()


def disconnect():
    """ Permet de se déconnecter """
    save("current_user", None)
    show_menu_principal()


def register():
    """ Permet de s'inscrire (uniquement pour créer un compte gestionnaire) """
    form_data = get_register_form()
    if form_data["admin_password"] != "12345678":
        print_error("Mot de passe administrateur incorrect")
    else:
        try:
            del form_data["admin_password"]
            Collaborator.create(affiliation=3, **form_data)
        except ValueError as e:
            sentry_sdk.capture_exception(e)
            print_error(str(e))
        except MySQLdb.IntegrityError as e:
            sentry_sdk.capture_exception(e)
            print_error("Email déja utilisée")
    show_menu_principal()


def create_collaborator():
    """ Permet de créer un collaborateur (uniquement par un gestionnaire) """
    form_data = get_create_collaborator_form()
    try:
        Collaborator.create(**form_data)
    except ValueError as e:
        sentry_sdk.capture_exception(e)
        print_error(str(e))    
    except MySQLdb.IntegrityError as e:
        sentry_sdk.capture_exception(e)
        print_error("Email déja utilisée") 
    show_menu_gestionnaire()


def update_collaborator():
    """ Permet de mettre à jour un collaborateur """
    form_data_email = get_find_collaborator_form()
    try:
        Collaborator.update(**form_data_email)
    except ValueError as e:
        print_error(str(e)) 
    except IndexError:
        print_error("Mauvais email")
    show_menu_gestionnaire()


def delete_collaborator():
    """ Permet de supprimer un utilisateur """
    form_data_email = get_find_collaborator_form()
    try:
        Collaborator.delete(**form_data_email)
    except IndexError:
        print_error("Mauvais email")
    show_menu_gestionnaire()
    
    
def create_client():
    """ Permet de créer un client """
    form_data = get_create_epic_client_form()
    try:
        EpicClient.create(contact_id=read("current_user").id, **form_data)
    except MySQLdb.IntegrityError:
        print_error("Email déja utilisée")
    show_menu_commercial()


def update_client():
    """Permet de mettre à jour un client """
    email = get_find_user_form()["email"]
    form_data = get_update_epic_client_form()
    try:
        EpicClient.update(email=email, **form_data)
    except IndexError:
        print_error("Identifiant introuvable")
    except MySQLdb.IntegrityError:
        print_error("Email déja utilisée")
    show_menu_commercial()
    
    
def delete_client():
    """ Permet de supprimer un client """
    form_data_email = get_find_user_form()
    try:
        EpicClient.delete(**form_data_email)
    except IndexError:
        print_error("Identifiant introuvable")
    show_menu_commercial()
    
    
def create_contract_gestion():
    """ Permet de créer un contrat """
    form_data = get_create_contract_form()
    Contract.create(contact_id=read("current_user").id, **form_data)
    show_menu_gestionnaire()
    
    
def update_contract_gestion():
    """ Permet de mettre à jour un contrat """
    form_data = get_id_form()
    try:
        Contract.update(**form_data)
    except IndexError:
        print_error("Identifiant introuvable\n")
    show_menu_gestionnaire()


def update_contract():
    """Permet de mettre à jour un contrat """
    form_data = get_id_form()
    try:
        Contract.update(**form_data)
    except IndexError as e:
        sentry_sdk.capture_exception(e)
        print_error("Identifiant introuvable\n")
    except ValueError as e:
        sentry_sdk.capture_exception(e)
        print_error(str(e))
    show_menu_commercial()
  
    
def delete_contract():
    """ Permet de supprimer un contrat """
    form_data = get_id_form()
    try:
        Contract.delete(**form_data)
    except IndexError as e:
        sentry_sdk.capture_exception(e)
        print_error("Identifiant introuvable")
    show_menu_commercial()


def create_event():
    """ Permet de créer un évènement """
    form_data = get_create_event_form()
    try:
        Event.create(**form_data)
    except ValueError as e:
        sentry_sdk.capture_exception(e)
        print_error(str(e))
    show_menu_commercial()
    
    
def update_event():
    """ Permet de mettre à jour un évènement """
    form_data = get_id_form()
    try:
        Event.update(**form_data)
    except IndexError as e:
        sentry_sdk.capture_exception(e)
        print_error("Identifiant introuvable")
    show_menu_support()
    
    
def assign_support_event():
    """ Permet d'assigner un support à un évènement """
    id = get_id_form()["id"]
    form_data = get_assign_support_event_form()
    try:
        Event.assign_support(id=id, **form_data)
    except IndexError as e:
        sentry_sdk.capture_exception(e)
        print_error("Identifiant introuvable")
    show_menu_gestionnaire()


def delete_event():
    """ Permet de supprimer un évènement """
    form_data = get_id_form()
    try:
        Event.delete(**form_data)
    except IndexError as e:
        sentry_sdk.capture_exception(e)
        print_error("Identifiant introuvable")
    show_menu_commercial()
