from utils import email_validator, password_validator, permission_validation, str_validator, telephone_validator, validate, int_validator


def create_user_obj():
    list_fields = [
        {"name": "nom", "description": "Entrer votre nom : ", "validators": str_validator},
        {"name": "password", "description": "Entrer votre mot de passe : ", "validators": password_validator},
        {"name": "email", "description": "Entrer votre email : ", "validators": email_validator},
    ]
    user_values = validate(list_fields)
    affiliation, permission = permission_validation()
    return user_values, affiliation, permission


def create_epic_client_objet():
    list_fields = [
        {"name": "nom", "description": "Entrer votre nom :", "validators": str_validator},
        {"name": "entreprise", "description": "Entrer le nom de l'entreprise : ", "validators": str_validator},
        {"name": "telephone", "description": "Entrer votre numéro de télephone : ", "validators": telephone_validator},
        {"name": "email", "description": "Entrer votre email: ", "validators": email_validator},
        {"name": "contact", "description": "Entrer votre contact: ", "validators": str_validator}]
    values_dict = validate(list_fields)
    return values_dict


def create_evenement_objet_update():
    list_fields = [
        {"name": "contrat_id", "description": "numéro du contrat ! ", "validators": str_validator},
        {"name": "client_name", "description": "nom du client ! ", "validators": str_validator},
        {"name": "client_contact", "description": "email du client ! ", "validators" : int_validator},
        {"name": "location", "description": "Description du lieu et précision ! ", "validators" : str_validator},
        {"name": "attendes", "description": "le nombre d'invités ? ", "validators" : int_validator},
        {"name": "NOTES", "description": "Notes de l'évenement ! ", "validators" : str_validator},]
    values_dict = validate(list_fields)
    return values_dict


def create_evenement_objet():
    list_fields = [
        {"name": "location", "description": "La location de l'évenement ? ", "validators": str_validator},
        {"name": "attendes", "description": "le nombre d'invités ? ", "validators" : int_validator},
        {"name": "NOTES", "description": "Description du lieu et précision !", "validators" : str_validator}]
    values_dict = validate(list_fields)
    return values_dict


def create_contrat_objet():
    list_fields = [
        {"name": "information_id", "description": "information client ? ", "validators": int_validator},
        {"name": "contact", "description": "information collaborater du client ? ", "validators": str_validator},
        {"name": "prix", "description": "prix du contrat ?", "validators": int_validator},
        {"name": "rest_prix", "description": "reste a payer du contrat ?", "validators": int_validator},
        {"name": "creation", "description": "creation du contrat ?", "validators": int_validator},
    ]
    values_dict = validate(list_fields)
    return values_dict
