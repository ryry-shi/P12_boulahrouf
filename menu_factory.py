from menu import Menu


def create_menu_factory(name):
    match name:
        case "PRINCIPAL":
            return lambda connect, register: Menu(
                "Menu principal", (
                    ("Se connecter", connect),
                    ("Créer un compte gestionnaire", register),
                    ("Quitter", print)
                )
            )
        case "GESTION":
            return lambda disconnect, read_only, create_collaborator, update_collaborator, delete_collaborator, create_contract_gestion, update_contract_gestion, assign_support_event: Menu(
                "Menu gestionnaire",
                (
                    ("Consulter la base de données", read_only),
                    ("Créer un collaborator", create_collaborator),
                    ("modifier un collaborator", update_collaborator),
                    ("Supprimer un collaborator", delete_collaborator),
                    ("Créer un contrat", create_contract_gestion),
                    ("Modifier un contrat", update_contract_gestion),
                    ("Associer un collaborateur support à un événement", assign_support_event),
                    ("Se déconnecter", disconnect)
                )
            )
        case "COMMERCIAL":
            return lambda disconnect, read_only, create_client, update_client, delete_client, update_contract, create_event, delete_event, read_non_signed_contracts: Menu(
                "Menu commercial",
                (
                    ("Consulter la base de données", read_only),
                    ("Consulter les contrats non signés", read_non_signed_contracts),
                    ("Créer un client", create_client),
                    ("Modifier un client qui m'est attribué", update_client),
                    ("Supprimer un client qui m'est attribué", delete_client),
                    ("Modifier un contrat qui m'est attribué", update_contract),
                    ("Supprimer un contrat qui m'est attribué", "delete_contract"),
                    ("Créer un événement pour un client qui a signé un contrat", create_event),
                    ("Supprimer un event", delete_event),
                    ("Se déconnecter", disconnect)
                )
            )
        case "SUPPORT":
            return lambda disconnect, read_only, update_event, read_support_events: Menu(
                "Menu support",
                (                
                    ("Consulter la base de données", read_only),
                    ("Consulter les évènements qui me sont attribués", read_support_events),
                    ("Mettre à jour un évènement qui m'est attribué", update_event),
                    ("Se déconnecter", disconnect)
                )
            )
        case "CONSULTER":
            return lambda read_clients, read_contracts, read_events: Menu(
            'Menu consultation',
            (               
                ("Consulter les clients", read_clients),
                ("Consulter les Contracts", read_contracts),
                ("Consulter les évenements", read_events),
                ("Retour", print)
            )
        )
            
