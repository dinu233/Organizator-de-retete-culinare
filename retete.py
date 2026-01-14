# retete.py
# Colegul 1 – gestionarea rețetelor

# Lista principală de rețete
retete = []


def adauga_reteta(nume, categorie, ingrediente, instructiuni):
    reteta_noua = {
        "nume": nume,
        "categorie": categorie,
        "ingrediente": ingrediente,
        "instructiuni": instructiuni
    }
    retete.append(reteta_noua)
    return reteta_noua


def sterge_reteta(nume):
    for reteta in retete:
        if reteta["nume"].lower() == nume.lower():
            retete.remove(reteta)
            return True
    return False


def editeaza_reteta(
    nume,
    nume_nou=None,
    categorie_noua=None,
    ingrediente_noi=None,
    instructiuni_noi=None
):
    for reteta in retete:
        if reteta["nume"].lower() == nume.lower():
            if nume_nou:
                reteta["nume"] = nume_nou
            if categorie_noua:
                reteta["categorie"] = categorie_noua
            if ingrediente_noi:
                reteta["ingrediente"] = ingrediente_noi
            if instructiuni_noi:
                reteta["instructiuni"] = instructiuni_noi
            return reteta
    return None

