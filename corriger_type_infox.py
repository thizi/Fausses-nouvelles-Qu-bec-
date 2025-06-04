import pandas as pd

# Fonction pour standardiser les types d'infox
def standardiser_type_infox(type_infox):
    # Convertir en chaîne et nettoyer
    type_infox = str(type_infox).strip().lower()
    
    # Dictionnaire de regroupement
    # Dictionnaire de regroupement mis à jour
    categories = {
        "désinformation": ["désinformation", "infox", "désinformation santé", "désinformation science", 
                        "infox politique", "infox scientifique", "infox santé", "infox économique", 
                        "infox environnement", "infox technologie", "désinformation scientifique", 
                        "infox médicale", "allégation erronée", "infox météo", "infox scolaire", 
                        "mésinformation (politique)", "mésinformation (rumeur)", 
                        "mésinformation (politiquement motivée)", "mésinformation"],
        
        "théorie_du_complot": ["théorie du complot", "complot / infox", "infox conspiration"],
        
        "rumeur": ["rumeur", "rumeur politique", "rumeur électorale", "rumeur savante", "rumeur mensongère", 
                "légende urbaine", "rumeur criminelle", "rumeur santé", "rumeur économique", 
                "rumeur financière", "rumeur scientifique", "rumeur urbaine", "rumeur antivax"],
        
        "canular": ["canular", "hoax", "canular / rumeur", "parodie / hoax", "canular visuel", 
                    "canular politique", "canular vidéo", "canular / hoax", "rumeur / hoax", 
                    "canular téléphonique", "canular sportif", "canular viral", "canular météorologique", 
                    "canular (photomontage)", "infox vidéo (canular)", "canular touristique", "hoax santé"],
        
        "arnaque": ["arnaque", "arnaque financière", "arnaque en ligne", "arnaque / fraude", 
                    "escroquerie/infox", "arnaque commerciale", "arnaque pub / infox", "canular/escroquerie"],
        
        "manipulation": ["manipulation", "manipulation visuelle", "manipulation médiatique", "deepfake", 
                        "hoax / harcèlement"],
        
        # La catégorie "satire" est supprimée et son contenu est déplacé ici
        "autre": ["mythe naturel", "alerte bidon", "information véridique", 
                "satire", "satire devenue virale", "infox parodique", "satire/canular"],
        
        "information_partielle": ["information partielle", "information incomplète"]
    }

    
    # Vérifier à quelle catégorie appartient le type
    for categorie, termes in categories.items():
        if any(terme in type_infox for terme in termes):
            return categorie.capitalize()
    
    # Par défaut, si aucun match, retourner "Autre"
    return "Autre"

# Charger le fichier Excel
fichier_excel = r"C:\Users\doghm\Desktop\projet-infox\last\alldata.xlsx"
try:
    df = pd.read_excel(fichier_excel)
    print("Colonnes dans le fichier :", df.columns.tolist())
except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_excel}' n'a pas été trouvé.")
    exit()

# Vérifier si la colonne 'type_d_infox' existe
if 'type_d_infox' not in df.columns:
    print("Erreur : La colonne 'type_d_infox' n'existe pas dans le fichier.")
    exit()

# Afficher quelques valeurs avant transformation
print("\nExemples de types avant transformation :")
print(df['type_d_infox'].head(10).to_list())

# Appliquer la fonction
df['type_d_infox'] = df['type_d_infox'].apply(standardiser_type_infox)

# Afficher quelques valeurs après transformation
print("\nExemples de types après transformation :")
print(df['type_d_infox'].head(10).to_list())

# Enregistrer dans un nouveau fichier
nouveau_fichier = r"C:\Users\doghm\Desktop\projet-infox\last\cleanData.xlsx"
df.to_excel(nouveau_fichier, index=False)
print(f"\nFichier '{nouveau_fichier}' créé avec les types d'infox corrigés.")