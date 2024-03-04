from menu import Menu


def create_menu_factory(name):
    match name:
        case "PRINCIPAL":
            return lambda connect, register: Menu(
                "Menu principal", (
                    ("Se connecter", connect),
                    ("S'enregistrer", register),
                    ("Quitter", print)
                )
            )
        case "GESTIONNAIRE":
            return lambda read_only, create_collaborator, update_collaborator, delete_collaborator, create_contract_gestion, update_contract_gestion, update_event: Menu(
                f"Menu gestionnaire",
                (
                    ("Consulter la base de données", read_only),
                    ("Créer un collaborator", create_collaborator),
                    ("modifier un collaborator", update_collaborator),
                    ("Supprimer un collaborator", delete_collaborator),
                    ("Créer un contrat", create_contract_gestion),
                    ("Modifier un contrat", update_contract_gestion),
                    ("Update pour associer un collaborateur support à un événement", print),
                    ("Retour", print)
                )
            )
        case "COMMERCIAL":
            return lambda read_only, create_client, update_client, delete_client, update_contract, create_event, delete_event: Menu(
                f"Menu commercial",
                (
                    ("Consulter la base de données", read_only),
                    ("Créer un client", create_client),
                    ("Modifier un client qui m'est attribué", update_client),
                    ("Supprimer un client qui m'est attribué", delete_client),
                    ("Modifier un contrat qui m'est attribué", update_contract),
                    ("Supprimer un contrat qui m'est attribué", "delete_contract"),
                    ("Créer un événement pour un client qui a signé un contrat", create_event),
                    ("Supprimer un event", delete_event),
                    ("Retour", print)
                )
            )
        case "SUPPORT":
            return lambda read_only, update_event: Menu(
                f"Menu support",
                (                
                    ("Consulter la base de données", read_only),
                    ("Mettre à jour un évènement qui m'est attribué", print),
                    ("Retour", print)
                )
            )
