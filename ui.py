# ui.py
from retete import retete, adauga_reteta, sterge_reteta, editeaza_reteta
from cautare import cauta_reteta_dupa_nume, filtreaza_dupa_categorie


def _citeste_lista_ingrediente():
    txt = input("Ingrediente (separate prin virgula): ").strip()
    if not txt:
        return []
    return [x.strip() for x in txt.split(",") if x.strip()]


def _afiseaza_reteta(r):
    if not r:
        print("Nu exista reteta.")
        return
    print("\n--- RETETA ---")
    print(f"Nume: {r.get('nume','')}")
    print(f"Categorie: {r.get('categorie','')}")
    ingr = r.get("ingrediente", [])
    if isinstance(ingr, list):
        print("Ingrediente:", ", ".join(map(str, ingr)))
    else:
        print("Ingrediente:", ingr)
    print("Instructiuni:", r.get("instructiuni",""))
    print("------------\n")


def _afiseaza_lista(lista):
    if not lista:
        print("Lista este goala.")
        return
    print("\n=== LISTA RETETE ===")
    for i, r in enumerate(lista, start=1):
        print(f"{i}. {r.get('nume','')} ({r.get('categorie','')})")
    print("====================\n")


def porneste_aplicatia():
    while True:
        print("===== ORGANIZATOR RETETE =====")
        print("1. Adauga reteta")
        print("2. Sterge reteta")
        print("3. Editeaza reteta")
        print("4. Afiseaza toate retetele")
        print("5. Cauta reteta dupa nume")
        print("6. Filtreaza dupa categorie")
        print("0. Iesire")
        opt = input("Alege o optiune: ").strip()

        if opt == "1":
            nume = input("Nume: ").strip()
            categorie = input("Categorie: ").strip()
            ingrediente = _citeste_lista_ingrediente()
            instructiuni = input("Instructiuni: ").strip()
            adauga_reteta(nume, categorie, ingrediente, instructiuni)
            print("✅ Reteta adaugata!\n")

        elif opt == "2":
            nume = input("Numele retetei de sters: ").strip()
            if sterge_reteta(nume):
                print("✅ Reteta stearsa!\n")
            else:
                print("❌ Nu am gasit reteta.\n")

        elif opt == "3":
            nume = input("Numele retetei de editat: ").strip()
            r = cauta_reteta_dupa_nume(nume)
            if not r:
                print("❌ Nu am gasit reteta.\n")
                continue

            print("Ce vrei sa modifici? (lasa gol ca sa pastrezi)")
            nume_nou = input("Nume nou: ").strip() or None
            categorie_noua = input("Categorie noua: ").strip() or None

            schimb_ing = input("Schimbi ingredientele? (da/nu): ").strip().lower()
            ingrediente_noi = _citeste_lista_ingrediente() if schimb_ing == "da" else None

            instructiuni_noi = input("Instructiuni noi: ").strip() or None

            rezultat = editeaza_reteta(
                nume,
                nume_nou=nume_nou,
                categorie_noua=categorie_noua,
                ingrediente_noi=ingrediente_noi,
                instructiuni_noi=instructiuni_noi
            )
            if rezultat:
                print("✅ Reteta actualizata!\n")
            else:
                print("❌ Nu s-a putut edita reteta.\n")

        elif opt == "4":
            _afiseaza_lista(retete)

        elif opt == "5":
            nume = input("Numele cautat: ").strip()
            _afiseaza_reteta(cauta_reteta_dupa_nume(nume))

        elif opt == "6":
            cat = input("Categoria: ").strip()
            rezultate = filtreaza_dupa_categorie(cat)
            _afiseaza_lista(rezultate)

        elif opt == "0":
            print("La revedere!")
            break

        else:
            print("❌ Optiune invalida.\n")
