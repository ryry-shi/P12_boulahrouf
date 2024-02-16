def val_function_int(value):
    list_number = list(range(1, 100))
    for i in range(1, 100):
        for y in list_number:
            if str(y) == value:
                return int(value)
        else:
            value = input("rentrer un id correcte")
