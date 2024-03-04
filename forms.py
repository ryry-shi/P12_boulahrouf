from typing import Dict, Any
from utils import email_validator, int_validator, password_validator, past_date_validator, phone_validator, positive_int_validator, str_validator, submit_form


def get_find_collaborator_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour trouver un collaborateur
    """
    return submit_form(
        "Trouver un collaborateur",
        [
            {"name": "email", "description": "email", "validator": email_validator}
        ]
    )


def get_login_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour se connecter à son compte utilisateur
    """
    return submit_form(
        "Se connecter",
        [
            {"name": "email", "description": "Email", "validator": email_validator},
            {"name": "password", "description": "Mot de passe", "validator": password_validator}
        ]
    )


def get_register_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour créer un compte utilisateur
    """
    return submit_form(
        "S'enregistrer",
        [
            {"name": "email", "description": "Email", "validator": email_validator},
            {"name": "name", "description": "name", "validator": str_validator},
            {"name": "password", "description": "Mot de passe", "validator": password_validator},
            {"name": "affiliation", "description": "Affiliation", "validator": positive_int_validator}
        ]
    )


def get_find_user_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour chercher un nouveau client
    """
    return submit_form(
        "Trouver un client",
        [
            {
                "name": "email", "description": "Email", "validator": email_validator,
            },
        ]
    )


def get_id_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour trouver un identifiant de contrat
    """
    return submit_form(
        "Trouver un identifiant",
        [
            {
                "name": "id", "description": "Identifiant", "validator": positive_int_validator
            }
        ]
    )


def get_create_collaborator_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour créer un nouveau collaborateur
    """
    return submit_form(
        "Créer un collaborateur",
        [
            {"name": "name", "description": "name", "validator": str_validator},
            {"name": "password", "description": "Mot de passe", "validator": password_validator},
            {"name": "email", "description": "Email", "validator": email_validator},
        ]
    )


def get_create_epic_client_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour créer un nouvel epic client
    """
    return submit_form(
        "Trouver un client",
        [
            {"name": "name", "description": "Nom", "validator": str_validator},
            {"name": "email", "description": "Email", "validator": email_validator},
            {"name": "phone", "description": "Numéro de télephone", "validator":phone_validator},
            {"name": "entreprise", "description": "Entreprise", "validator": str_validator},
            {"name": "creation_date", "description": "Date de création", "validator": past_date_validator},
        ]
    )
  
    
def get_update_epic_client_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour mettre a jour un epic client
    """
    return submit_form(
        "Mettre à jour un client",
        [
            {"name": "name", "description": "Nom", "validator": str_validator},
            {"name": "email", "description": "Email", "validator": email_validator},
            {"name": "phone", "description": "Numéro de télephone", "validator":phone_validator},
            {"name": "entreprise", "description": "Entreprise", "validator": str_validator},
        ]
    )


def get_create_contract_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour créer un contrat
    """
    return submit_form(
        "Créer un contrat",
        [
            {"name": "epic_client", "description": "Identifiant du client", "validator": int_validator},
            {"name": "amount", "description": "Montant", "validator": int_validator},
            {"name": "remaining_amount", "description": "Reste à payer", "validator": int_validator},
            {"name": "creation_date", "description": "Date de création", "validator": past_date_validator},
        ]
    )
    
    
def get_update_contract_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour créer un contrat
    """
    return submit_form(
        "Modifier un contrat",
        [
            {"name": "epic_client", "description": "Identifiant du client", "validator": int_validator},
            {"name": "amount", "description": "Montant", "validator": int_validator},
            {"name": "remaining_amount", "description": "Reste à payer", "validator": int_validator},
        ]
    )


def get_create_event_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour créer un évènement
    """
    return submit_form(
        "Créer un évènement",
        [
            {"name": "contrat_id", "description": "Contrat", "validator": int_validator},
            {"name": "event_start", "description": "Début", "validator": past_date_validator},
            {"name": "event_end", "description": "Fin", "validator": past_date_validator},
            {"name": "support_contact", "description": "Contact", "validator": str_validator},
            {"name": "location", "description": "location", "validator": str_validator},
            {"name": "attendes", "description": "attendes", "validator" : int_validator},
            {"name": "notes", "description": "Description", "validator" : str_validator}
        ]
    )


def get_update_event_form() -> Dict[str, str | Any]:
    """
        Retourne un formulaire pour créer un évènement
    """
    return submit_form(
        "Mettre à jour un évènement",
        [
            {"name": "contrat_id", "description": "Contrat", "validator": int_validator},
            {"name": "client_name", "description": "Nom", "validator": str_validator},
            {"name": "client_email", "description": "Email", "validator": email_validator},
            {"name": "event_start", "description": "Début", "validator": past_date_validator},
            {"name": "event_end", "description": "Fin", "validator": past_date_validator},
            {"name": "support_contact", "description": "Contact", "validator": str_validator},
            {"name": "location", "description": "location", "validator": str_validator},
            {"name": "attendes", "description": "attendes", "validator" : int_validator},
            {"name": "notes", "description": "Description", "validator" : str_validator}
        ]
    )