
import tkinter as tk
from tkinter import messagebox

from retete import retete, adauga_reteta, sterge_reteta, editeaza_reteta
from cautare import cauta_reteta_dupa_nume, filtreaza_dupa_categorie


class RecipeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizator de rețete")
        self.geometry("900x520")
        self.minsize(850, 480)

        self._build_ui()
        self.refresh_list()

    def _build_ui(self):
        # Layout: stânga listă, dreapta formular + butoane
        left = tk.Frame(self, padx=10, pady=10)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        right = tk.Frame(self, padx=10, pady=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- LISTĂ REȚETE (stânga) ---
        tk.Label(left, text="Rețete", font=("Arial", 12, "bold")).pack(anchor="w")

        self.listbox = tk.Listbox(left, width=35, height=22)
        self.listbox.pack(fill=tk.BOTH, expand=False, pady=(6, 6))
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        btns_left = tk.Frame(left)
        btns_left.pack(fill=tk.X, pady=(4, 0))

        tk.Button(btns_left, text="Refresh", command=self.refresh_list).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(btns_left, text="Șterge selectată", command=self.delete_selected).pack(side=tk.LEFT)

        # --- FORMULAR (dreapta) ---
        tk.Label(right, text="Detalii rețetă", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")

        tk.Label(right, text="Nume:").grid(row=1, column=0, sticky="e", pady=4)
        self.entry_nume = tk.Entry(right, width=40)
        self.entry_nume.grid(row=1, column=1, columnspan=2, sticky="w", pady=4)

        tk.Label(right, text="Categorie:").grid(row=2, column=0, sticky="e", pady=4)
        self.entry_categorie = tk.Entry(right, width=40)
        self.entry_categorie.grid(row=2, column=1, columnspan=2, sticky="w", pady=4)

        tk.Label(right, text="Ingrediente (virgule):").grid(row=3, column=0, sticky="e", pady=4)
        self.entry_ingrediente = tk.Entry(right, width=40)
        self.entry_ingrediente.grid(row=3, column=1, columnspan=2, sticky="w", pady=4)

        tk.Label(right, text="Instrucțiuni:").grid(row=4, column=0, sticky="ne", pady=4)
        self.text_instr = tk.Text(right, width=60, height=10)
        self.text_instr.grid(row=4, column=1, columnspan=2, sticky="w", pady=4)

        # --- BUTOANE CRUD ---
        crud = tk.Frame(right, pady=10)
        crud.grid(row=5, column=0, columnspan=3, sticky="w")

        tk.Button(crud, text="Adaugă", width=12, command=self.add_recipe).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(crud, text="Editează", width=12, command=self.edit_recipe).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(crud, text="Curăță câmpuri", width=14, command=self.clear_fields).pack(side=tk.LEFT)

        # --- CĂUTARE / FILTRARE ---
        tk.Label(right, text="Căutare / Filtrare", font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=3, sticky="w", pady=(10, 0))

        tk.Label(right, text="Caută după nume:").grid(row=7, column=0, sticky="e", pady=4)
        self.entry_cauta_nume = tk.Entry(right, width=30)
        self.entry_cauta_nume.grid(row=7, column=1, sticky="w", pady=4)
        tk.Button(right, text="Caută", command=self.search_by_name).grid(row=7, column=2, sticky="w", padx=8)

        tk.Label(right, text="Filtrează categorie:").grid(row=8, column=0, sticky="e", pady=4)
        self.entry_filtru_cat = tk.Entry(right, width=30)
        self.entry_filtru_cat.grid(row=8, column=1, sticky="w", pady=4)
        tk.Button(right, text="Filtrează", command=self.filter_by_category).grid(row=8, column=2, sticky="w", padx=8)

        tk.Button(right, text="Arată toate", command=self.refresh_list).grid(row=9, column=1, sticky="w", pady=(6, 0))

        # Spațiere grid
        right.grid_columnconfigure(1, weight=1)

    def _ingrediente_list(self):
        txt = self.entry_ingrediente.get().strip()
        if not txt:
            return []
        return [x.strip() for x in txt.split(",") if x.strip()]

    def _get_instr_text(self):
        return self.text_instr.get("1.0", "end").strip()

    def clear_fields(self):
        self.entry_nume.delete(0, tk.END)
        self.entry_categorie.delete(0, tk.END)
        self.entry_ingrediente.delete(0, tk.END)
        self.text_instr.delete("1.0", "end")

    def refresh_list(self, lista=None):
        self.listbox.delete(0, tk.END)
        data = lista if lista is not None else retete
        for r in data:
            self.listbox.insert(tk.END, f"{r.get('nume','')} ({r.get('categorie','')})")

    def on_select(self, _event=None):
        if not self.listbox.curselection():
            return
        idx = self.listbox.curselection()[0]
        # Dacă e filtrată lista, idx se raportează la ce e afișat. Ca să rămână simplu,
        # încărcăm după nume (care e unic în proiectele voastre, de obicei).
        item = self.listbox.get(idx)
        nume = item.split(" (", 1)[0].strip()
        r = cauta_reteta_dupa_nume(nume)
        if not r:
            return

        self.clear_fields()
        self.entry_nume.insert(0, r.get("nume", ""))
        self.entry_categorie.insert(0, r.get("categorie", ""))

        ingr = r.get("ingrediente", [])
        if isinstance(ingr, list):
            self.entry_ingrediente.insert(0, ", ".join(map(str, ingr)))
        else:
            self.entry_ingrediente.insert(0, str(ingr))

        self.text_instr.insert("1.0", r.get("instructiuni", ""))

    def add_recipe(self):
        nume = self.entry_nume.get().strip()
        categorie = self.entry_categorie.get().strip()
        ingrediente = self._ingrediente_list()
        instructiuni = self._get_instr_text()

        if not nume or not categorie:
            messagebox.showwarning("Lipsesc date", "Completează cel puțin: nume și categorie.")
            return

        adauga_reteta(nume, categorie, ingrediente, instructiuni)
        self.refresh_list()
        messagebox.showinfo("Succes", "Rețeta a fost adăugată.")

    def delete_selected(self):
        if not self.listbox.curselection():
            messagebox.showwarning("Selectează", "Selectează o rețetă din listă.")
            return
        idx = self.listbox.curselection()[0]
        item = self.listbox.get(idx)
        nume = item.split(" (", 1)[0].strip()

        if messagebox.askyesno("Confirmare", f"Ștergi rețeta: {nume}?"):
            ok = sterge_reteta(nume)
            self.refresh_list()
            self.clear_fields()
            messagebox.showinfo("Rezultat", "Ștearsă." if ok else "Nu am găsit rețeta.")

    def edit_recipe(self):
        nume_vechi = self.entry_nume.get().strip()
        if not nume_vechi:
            messagebox.showwarning("Lipsă nume", "Selectează o rețetă sau scrie numele ei în câmp.")
            return

        # În proiectul vostru, editează după nume (nume_vechi).
        # Dacă vrei să schimbi numele, îl citim tot de aici.
        nume_nou = self.entry_nume.get().strip() or None
        categorie_noua = self.entry_categorie.get().strip() or None
        ingrediente_noi = self._ingrediente_list()
        instructiuni_noi = self._get_instr_text() or None

        rezultat = editeaza_reteta(
            nume_vechi,
            nume_nou=nume_nou,
            categorie_noua=categorie_noua,
            ingrediente_noi=ingrediente_noi,
            instructiuni_noi=instructiuni_noi
        )
        if rezultat:
            self.refresh_list()
            messagebox.showinfo("Succes", "Rețeta a fost actualizată.")
        else:
            messagebox.showerror("Eroare", "Nu am găsit rețeta pentru editare.")

    def search_by_name(self):
        nume = self.entry_cauta_nume.get().strip()
        if not nume:
            messagebox.showwarning("Lipsă", "Scrie un nume pentru căutare.")
            return
        r = cauta_reteta_dupa_nume(nume)
        if not r:
            messagebox.showinfo("Rezultat", "Nu am găsit rețeta.")
            return
        self.refresh_list([r])

    def filter_by_category(self):
        cat = self.entry_filtru_cat.get().strip()
        if not cat:
            messagebox.showwarning("Lipsă", "Scrie o categorie pentru filtrare.")
            return
        rezultate = filtreaza_dupa_categorie(cat)
        self.refresh_list(rezultate)


def porneste_gui():
    app = RecipeApp()
    app.mainloop()
