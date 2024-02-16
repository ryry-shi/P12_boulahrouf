def validate_prix():
    prix = int(input("Quel est le prix ? (un entier)"))
    rest_prix = int(input("Que rest'il a payer ? (un entier)"))
    while True:
        if prix > rest_prix:
            break
        else:
            prix = input("Quel est le prix ? ")
            rest_prix = input("Que rest'il a payer ? ")
    return prix, rest_prix
