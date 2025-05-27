import pandas as pd
import re

# Fonction pour standardiser les dates avec débogage
def standardiser_date(date):
    print(f"Date originale : '{date}'")  # Débogage : affiche la date brute
    # Convertir en chaîne et nettoyer
    date = str(date).strip()
    
    # Cas 1 : "Inconnue" ou vide
    if date.lower() in ["inconnue", "nan", "", "none"]:
        print(f"-> Transformé en : 'N'")
        return "N"
    
    # Cas 2 : Date complète (ex. "2021-09-22 00:00:00" ou "2021-09-22")
    try:
        date_obj = pd.to_datetime(date, errors='raise')
        result = date_obj.strftime("%d/%m/%Y")
        print(f"-> Transformé en : '{result}'")
        return result
    except:
        pass
    
    # Cas 3 : Année seule (ex. "2019")
    if re.match(r"^\d{4}$", date):
        result = f"01/01/{date}"
        print(f"-> Transformé en : '{result}'")
        return result
    
    # Cas 4 : Année et mois (ex. "2023-04" ou "2023-04 (avril)")
    if re.match(r"^\d{4}-\d{2}.*$", date):
        annee_mois = date.split()[0]  # Prendre "2023-04" si texte suit
        annee, mois = annee_mois.split("-")
        result = f"01/{mois}/{annee}"
        print(f"-> Transformé en : '{result}'")
        return result
    
    # Cas par défaut : non reconnu
    print(f"-> Non reconnu, transformé en : 'N'")
    return "N"

# Charger le fichier Excel
fichier_excel = "infox_corrige.xlsx"
try:
    df = pd.read_excel(fichier_excel)
    print("Colonnes dans le fichier :", df.columns.tolist())  # Débogage : affiche les colonnes
except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_excel}' n'a pas été trouvé.")
    exit()

# Vérifier si la colonne 'date_de_repérage' existe
if 'date_de_repérage' not in df.columns:
    print("Erreur : La colonne 'date_de_repérage' n'existe pas dans le fichier.")
    exit()

# Afficher quelques dates avant transformation
print("\nExemples de dates avant transformation :")
print(df['date_de_repérage'].head(10).to_list())

# Appliquer la fonction
df['date_de_repérage'] = df['date_de_repérage'].apply(standardiser_date)

# Afficher quelques dates après transformation
print("\nExemples de dates après transformation :")
print(df['date_de_repérage'].head(10).to_list())

# Enregistrer dans un nouveau fichier
nouveau_fichier = "infox_dates_corrigees.xlsx"
df.to_excel(nouveau_fichier, index=False)
print(f"\nFichier '{nouveau_fichier}' créé avec les dates corrigées.")