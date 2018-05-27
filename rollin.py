def somme_chiffre(nb:int) -> int:
    return sum(map(int, str(nb).replace('-', '').replace('.', '')))

def rollin(annee) -> int:
    """Calcule le nombre de Rollin pour l'année donnée

    >>> rollin(2005)
    3
    >>> rollin(1922)
    5
    >>> rollin(0)
    0

    """
    nb = ((-52 * annee) + (sum(map(int, str(annee)[1:])) * 21947)) / 73
    while len(str(nb)) > 1:
        nb = somme_chiffre(nb)
    return nb

assert rollin(2005) == 3
assert rollin(1922) == 5
