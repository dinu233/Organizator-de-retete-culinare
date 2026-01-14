# cautare.py
from retete import retete


def cauta_reteta_dupa_nume(nume):
    """
    Caută o rețetă după nume (case-insensitive)
    Returnează rețeta sau None
    """
    for reteta in retete:
        if reteta["nume"].lower() == nume.lower():
            return reteta
    return None


def filtreaza_dupa_categorie(categorie):
    """
    Returnează o listă cu rețete dintr-o anumită categorie
    """
    rezultate = []
    for reteta in retete:
        if reteta["categorie"].lower() == categorie.lower():
            rezultate.append(reteta)
    return rezultate
