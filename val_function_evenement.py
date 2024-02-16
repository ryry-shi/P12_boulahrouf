import datetime


def validate_value_two_date(message, message_two):
    datetime_start_evenement = datetime.datetime.fromisoformat(input(message))
    datetime_end_evenement = datetime.datetime.fromisoformat(input(message_two))
    while True:
        if datetime_start_evenement < datetime_end_evenement:
            break
        else:
            datetime_start_evenement = input("Les dates sont incorrecte! Veuillez entrez des dates correctes!! ")
            datetime_end_evenement = input("La date de fin de l'évènement n'est pas correcte ! ")
    return datetime_start_evenement, datetime_end_evenement


def validate_value_date_contrat():
    while True:
        date = input("la création du contrat ? ")
        date_value = datetime.datetime.fromisoformat(date)
        if date_value < datetime.datetime.today():
            return date_value
        else:
            date = input("la date de création n'est pas correcte ! ")
