import bcrypt


def validate_value_date_user():
    username = input("Choissisez votre nom ? ")
    while len(username) < 6:
        if username == str and len(username) > 14:
            break
        else:
            print("Votre nom est trop court")
            username = input("")
    password = input("Choissisez votre mot de passe ? ")
    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return username, password
