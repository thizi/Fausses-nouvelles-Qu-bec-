import pandas as pd

# Fonction pour standardiser les thématiques
def standardiser_thematique(thematique):
    # Convertir en chaîne et nettoyer
    thematique = str(thematique).strip().lower()
    
    # Corriger les erreurs typographiques
    if thematique == "sané":
        thematique = "santé"
    
    # Dictionnaire de regroupement
    categories = {
        "Santé": ["santé", "santé publique", "santé (covid-19)", "santé/vaccination", "santé/médecine", 
                  "santé/politique", "santé/technologie", "santé/éducation", "santé/consommation", 
                  "santé/environnement", "santé/nutrition", "santé/démographie", "santé – vaccination", 
                  "santé – protection", "santé – thérapeutique", "santé - grand public", 
                  "criminologie / santé", "technologie/santé", "conspiration/santé", "santé animale"],
        "Politique": ["politique", "politique (élections)", "politique fédérale", "politique locale", 
                     "politique/santé", "politique/économie", "politique/culture", "politique/société", 
                     "politique/médias", "politique/éducation", "politique/religion", "politique/minorités", 
                     "politique/langue", "politique/tourisme", "politique internationale", 
                     "géopolitique/sécurité", "sport/politique", "politique / élection"],
        "Immigration": ["immigration", "immigration / religion", "immigration et finances" ,"immigration – économie" , "immigration – politique", "immigration – langue, emploi" , "immigration – identité, langue" , "immigration – démographie" , "immigration – économie", "immigration – sécurité" , "immigration – religion" , "asile/immigr."],
        "Économie": ["économie", "finance", "économie/politique", "économie/finance", "économie/énergie", 
                    "économie/religion", "immobilier", "consommation", "consommation/internet", 
                    "rumeur financière"],
        "Environnement": ["environnement", "climat", "environnement/santé", "environnement/climat", 
                         "biodiversité", "environnement/tourisme", "environnement/énergie", 
                         "environnement/conspiration", "nature/environnement", "climatologie"],
        "Sécurité": ["sécurité", "sécurité publique", "criminalité", "sécurité / forces de l’ordre", 
                    "sécurité / crime", "sécurité civile", "faits divers (criminalité)", "terrorisme/islamophobie"],
        "Éducation": ["éducation", "éducation/religion", "éducation/politique", "éducation/argent", 
                     "éducation/technologie", "éducation/vie privée", "éducation/identité", "éducation/média local"],
        "Technologie": ["technologie", "ia", "technologie/santé", "technologie/politique", 
                       "technologie/faits divers", "technologie/sécurité", "technologie/divertissement"],
        "Culture": ["culture", "société/culture", "célébrités/sociaux", "culture/politique", "culture/tourisme"],
        "Société": ["société", "société/éducation", "société/environnement", 
                   "politique/minorités", "langue", "société (traditions)"],
        "Médias": ["médias", "politique/médias", "média local", "infox médiatique"],
        "Autres": ["satire", "divertissement", "loisirs/environnement", "sport", "sport / covid-19", 
                   "politique municipale", "faits divers (accident)", "laïcité", "fédéralisme", 
                   "fiscalité", "science/justice", "science/catastrophe", "politique sociale", "urbanisme/environnement"]
    }
    
    # Vérifier à quelle catégorie appartient la thématique
    for categorie, termes in categories.items():
        if any(terme in thematique for terme in termes):
            return categorie
    
    # Par défaut, si aucun match, retourner "Autres"
    return "Autres"

# Charger le fichier Excel
fichier_excel = "infox_types_corriges.xlsx"
try:
    df = pd.read_excel(fichier_excel)
    print("Colonnes dans le fichier :", df.columns.tolist())
except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_excel}' n'a pas été trouvé.")
    exit()

# Vérifier si la colonne 'thématique' existe
if 'thématique' not in df.columns:
    print("Erreur : La colonne 'thématique' n'existe pas dans le fichier.")
    exit()

# Afficher quelques valeurs avant transformation
print("\nExemples de thématiques avant transformation :")
print(df['thématique'].head(10).to_list())

# Appliquer la fonction
df['thématique'] = df['thématique'].apply(standardiser_thematique)

# Afficher quelques valeurs après transformation
print("\nExemples de thématiques après transformation :")
print(df['thématique'].head(10).to_list())

# Enregistrer dans un nouveau fichier
nouveau_fichier = "infox_thematiques_corrigees.xlsx"
df.to_excel(nouveau_fichier, index=False)
print(f"\nFichier '{nouveau_fichier}' créé avec les thématiques corrigées.")