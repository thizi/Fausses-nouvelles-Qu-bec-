import pandas as pd

# Fonction pour standardiser les zones géographiques
def standardiser_zone_geographique(zone):
    # Convertir en chaîne et nettoyer
    zone = str(zone).strip().lower().replace("/ ", "/").replace(" ,", ",").replace(", ", ",")
        
    # Dictionnaire de regroupement
    categories = {
        "Québec (province)": ["québec", "montréal", "laval", "gatineau", "sherbrooke", "trois-rivières", 
                             "saguenay", "longueuil", "lévis", "saint-jérôme", "drummondville", "blainville", 
                             "chicoutimi", "granby", "mascouche", "val-d'or", "saint-hyacinthe", 
                             "alma (saguenay)", "bonaventure, gaspésie", "abitibi-témiscamingue", 
                             "québec (général)", "saguenay–lac-saint-jean", "trois-pistoles", "laurentides", 
                             "outaouais", "coteau-du-lac (montérégie)", "saint-georges (chaudière-appalaches)", 
                             "montréal-nord", "montréal (ville-marie)", "montréal (saint-michel)", 
                             "québec (ville)", "québec (secteur saint-roch)", "saint-jean-sur-richelieu", 
                             "rimouski", "charlevoix", "montréal-est", "dorval (montréal)", 
                             "la sarre (abitibi)", "alma (saguenay–lac-st-jean)", "lévis (québec)", 
                             "montréal (qc)"],
        "Canada": ["canada", "canada francophone", "canada/mondial", "nord du canada (médias sociaux francophones)", 
                   "québec/canada", "québec/canada francophone", "canada (résident québec ciblé via média local)"],
        "Monde francophone": ["monde francophone (incluant québec/canada)", "france et pays francophones (incl. québec)"],
        "International": ["international (contenu anglophone repris en fr.)", "états-unis, relayé en france/canada", 
                         "canada/monde", "monde (relayé au québec)"],
        "Autres": ["italie", "chine"]
    }
    
    # Vérifier à quelle catégorie appartient la zone
    for categorie, termes in categories.items():
        if any(terme in zone for terme in termes):
            return categorie
    
    # Par défaut, si aucun match, retourner "Autres"
    return "Autres"

# Charger le fichier Excel
fichier_excel = "infox_plateformes_corrigees.xlsx"
try:
    df = pd.read_excel(fichier_excel)
    print("Colonnes dans le fichier :", df.columns.tolist())
except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_excel}' n'a pas été trouvé.")
    exit()

# Vérifier si la colonne 'zone_geographique' existe
if 'zone_geographique' not in df.columns:
    print("Erreur : La colonne 'zone_geographique' n'existe pas dans le fichier.")
    exit()

# Afficher quelques valeurs avant transformation
print("\nExemples de zones géographiques avant transformation :")
print(df['zone_geographique'].head(10).to_list())

# Appliquer la fonction
df['zone_geographique'] = df['zone_geographique'].apply(standardiser_zone_geographique)

# Afficher quelques valeurs après transformation
print("\nExemples de zones géographiques après transformation :")
print(df['zone_geographique'].head(10).to_list())

# Enregistrer dans un nouveau fichier
nouveau_fichier = "infox_zones_corrigees.xlsx"
df.to_excel(nouveau_fichier, index=False)
print(f"\nFichier '{nouveau_fichier}' créé avec les zones géographiques corrigées.")