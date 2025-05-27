import pandas as pd

# Fonction pour standardiser la véracité
def standardiser_veracite(veracite):
    # Convertir en chaîne et nettoyer
    veracite = str(veracite).strip().lower()
    
    categories = {
        "FAUX": ["faux", "fausse", "fausses", "fausse nouvelle", "fausses nouvelles"],
        "TROMPEUR": ["trompeur"],
        "MANIPULÉ": ["manipulé"],
        "PARTIELLEMENT VRAI": ["partiellement vrai", "nuancé", "vrai, mais incomplet"],
        "VRAI": ["vrai"]
    }
    
    # Vérifier si la véracité commence par une catégorie connue
    for categorie, termes in categories.items():
        if veracite.startswith(categorie.lower()) or any(terme in veracite for terme in termes):
            return categorie
    
    # Par défaut, si aucun match, retourner "FAUX" (car la majorité des entrées sont fausses)
    return "FAUX"

# Charger le fichier Excel
fichier_excel = "infox_formats_corriges.xlsx"
try:
    df = pd.read_excel(fichier_excel)
    print("Colonnes dans le fichier :", df.columns.tolist())
except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_excel}' n'a pas été trouvé.")
    exit()

# Vérifier si la colonne 'véracité' existe
if 'véracité' not in df.columns:
    print("Erreur : La colonne 'véracité' n'existe pas dans le fichier.")
    exit()

# Afficher quelques valeurs avant transformation
print("\nExemples de véracité avant transformation :")
print(df['véracité'].head(10).to_list())

# Appliquer la fonction
df['véracité'] = df['véracité'].apply(standardiser_veracite)

# Afficher quelques valeurs après transformation
print("\nExemples de véracité après transformation :")
print(df['véracité'].head(10).to_list())

# Enregistrer dans un nouveau fichier
nouveau_fichier = "infox_veracite_corrige.xlsx"
df.to_excel(nouveau_fichier, index=False)
print(f"\nFichier '{nouveau_fichier}' créé avec les véracités corrigées.")