def RepresentsInt(inteiro):  # verificar se uma variavel represnta um numero inteiro
    try:
        int(inteiro)
        return True
    except ValueError:
        return False
