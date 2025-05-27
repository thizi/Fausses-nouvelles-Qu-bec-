import pandas as pd

# Fonction pour standardiser les sources de vérification
def standardiser_source_de_verification(source):
    # Convertir en chaîne et nettoyer
    source = str(source).strip().lower().replace(",", " / ").replace(";", " / ").replace("via", "&")
    
    # Corriger les erreurs typographiques
    source = source.replace("jouranl de québec", "journal de québec").replace("montréa", "montréal")
    
    # Supprimer les URLs
    for url in ["tvanouvelles.ca", "journaldequebec.com", "journaldemontreal.com", 
                "courrierlaval.com", "globalnews.ca"]:
        source = source.replace(url, "")
    
    # Gérer les sources sans information
    if any(term in source for term in ["aucune source officielle", "aucune source spécifique disponible", 
                                       "source média requise"]):
        return "N"
    
    # Dictionnaire de regroupement pour les sources répétées et uniques
    categories = {
        "TVA Nouvelles": ["tva nouvelles", "tva nlle", "tva (nouvelles)", "tva nlles", 
                          "tva nouvelles (qmi)", "tva nouvelles (24h)", "tva nouvelles (cic)", 
                          "tva nouvelles (journal de montréal)", "tva nouvelles (agence qmi)", 
                          "tva nouvelles (emmanuel dubourg)"],
        "Journal de Montréal": ["journal de montréal", "journal de montreal", "journal de montréa", 
                               "journal de montréal (agence qmi)", "journal de montréal (bureau enquête)", 
                               "journal de montréal (media qmi)"],
        "Journal de Québec": ["journal de québec", "le journal de québec", "journal de quebec", 
                             "journal de québec (qmi)", "journal de québec (afp)"],
        "Agence Science-Presse": ["agence science-presse", "science presse", "science-presse" ,"détecteur de rumeurs" ,"sciencepresse", 
                                 "agence science-presse (détecteur de rumeurs)", 
                                 "détecteur de rumeurs (science-presse)", 
                                 "détecteur de rumeurs (science presse)", 
                                 "détecteur de rumeurs (scientifique en chef du québec)", 
                                 "agence science-presse (données statistique qc)", 
                                 "agence science-presse (emploi-québec, statistique qc)", 
                                 "agence science-presse (statistique canada, unhcr)", 
                                 "agence science-presse (min. qc, sondages)"],
        "Radio-Canada": ["radio-canada", "radio-canada info", "radio-canada (vérif)", 
                        "radio-canada (saguenay)", "radio-canada «vrai ou faux»", 
                        "radio-canada vérification", "cbc décrypteurs (radio-canada)", 
                        "radio-canada (vér)"],
        "AFP Factuel": ["afp factuel", "afp", "afp & journal de montréal", "journal de québec & afp", 
                       "afp factuel (& defacto.fr)", "libération ou afp"],
        "La Presse": ["la presse", "la presse (vérification)", "la presse (satire)"],
        "Le Devoir": ["le devoir", "le devoir (vérification)"],
        "Wikipédia": ["wikipédia", "wikipedia"],
        "Elections Canada": ["elections canada", "elections canada & afp fact check", 
                            "elections canada & afp fact check (via dfrlab)"],
        "Statistique Canada": ["statistique canada"],
        "Santé Canada": ["santé canada"],
        "Ministère de l’Éducation du Québec": ["ministère de l’éducation du québec"],
        "Services aux Autochtones Canada": ["services aux autochtones canada"],
        "Finances Canada": ["finances canada"],
        "Banque du Canada": ["banque du canada"],
        "Rapport Environnement Canada": ["rapport environnement canada"],
        "Élections Québec": ["élections québec"],
        "Service de Police de Gatineau": ["service de police de la ville de gatineau (spvg)", 
                                         "journal de montréal (agence qmi, spvq)"],
        "IRCC": ["ircc (ministère immigration)", "ircc &"],
        "Conseil canadien pour les réfugiés": ["conseil canadien pour les réfugiés", 
                                             "conseil canadien pour les réfugiés (ccr)"],
        "Espace pour la vie": ["espace pour la vie (biodôme)"],
        "The Guardian": ["the guardian"],
        "Associated Press": ["associated press (fact-check)"],
        "Global News": ["global news", "global news canada", "global news (ap via canadian press)"],
        "HuffPost": ["huffpost"],
        "FactCheck.org": ["factcheck.org"],
        "Reuters Fact Check": ["reuters fact check"],
        "CityNews Montréal": ["citynews montréal"],
        "Le Soleil": ["le soleil (vérification)"],
        "Le Nouvelliste": ["le nouvelliste"],
        "Cult MTL": ["cult mtl"],
        "NewsGuard": ["newsguard"],
        "Vingt55": ["vingt55 (info locale)", "vingt55 (info local)"],
        "Viva Média": ["viva média (via rimq)" ,"viva média (via RIMQ)" ],
        "EnBeauce": ["enbeauce (journal régional)"],
        "Journal Ma Côte-Nord": ["journal ma côte-nord"],
        "Journal La Tribune": ["journal la tribune"],
        "BBC Afrique": ["bbc afrique"],
        "Exemplaire ULaval": ["exemplaire ulaval"],
        "Facebook": ["facebook"],
        "TikTok": ["tiktok"],
        "Canada.ca": ["canada.ca"],
        "Media Ecosystem Observatory": ["media ecosystem observatory"],
        "McGill Office Science & Société": ["mcgill (office science & société)"],
        "IRIS": ["institut de recherche iris (analyses)"],
        "Document universitaire": ["document universitaire de lutte anti-rumeurs"],
        "Rapport du budget fédéral": ["rapport du budget fédéral"],
        "Courrier Laval": ["courrier lavalcourrierlaval.comcourrierlaval.com"]
    }
    
    # Vérifier à quelle catégorie appartient la source
    for categorie, termes in categories.items():
        if any(terme in source for terme in termes):
            return categorie
    
    # Par défaut, retourner "N" si aucune source spécifique
    return "N"

# Charger le fichier Excel
fichier_excel = "infox_veracite_corrige.xlsx"
try:
    df = pd.read_excel(fichier_excel)
    print("Colonnes dans le fichier :", df.columns.tolist())
except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_excel}' n'a pas été trouvé.")
    exit()

# Vérifier si la colonne 'source_de_verification' existe
if 'source_de_verification' not in df.columns:
    print("Erreur : La colonne 'source_de_verification' n'existe pas dans le fichier.")
    exit()

# Afficher quelques valeurs avant transformation
print("\nExemples de sources avant transformation :")
print(df['source_de_verification'].head(10).to_list())

# Appliquer la fonction
df['source_de_verification'] = df['source_de_verification'].apply(standardiser_source_de_verification)

# Afficher quelques valeurs après transformation
print("\nExemples de sources après transformation :")
print(df['source_de_verification'].head(10).to_list())

# Enregistrer dans un nouveau fichier
nouveau_fichier = "infox_sources_nommees_corrigees.xlsx"
df.to_excel(nouveau_fichier, index=False)
print(f"\nFichier '{nouveau_fichier}' créé avec les sources de vérification corrigées.")