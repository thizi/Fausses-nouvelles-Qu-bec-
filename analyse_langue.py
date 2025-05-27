import pandas as pd

# Chemin vers le fichier Excel
file_path = 'analyse_impact_simplifiee.xlsx'

# Vérifier les noms des feuilles dans le fichier Excel
try:
    excel_file = pd.ExcelFile(file_path)
    print("Feuilles disponibles dans le fichier Excel :", excel_file.sheet_names)
except FileNotFoundError:
    print(f"Erreur : Le fichier '{file_path}' n'a pas été trouvé. Vérifiez le chemin du fichier.")
    exit()

# Lire le fichier Excel
# Remplacez 'Sheet1' par le nom correct de la feuille (ex. 'Feuille1')
sheet_name = 'Données'  # Mettez à jour avec le nom correct après avoir vérifié
try:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
except ValueError as e:
    print(f"Erreur : {e}. Vérifiez le nom de la feuille avec la liste ci-dessus.")
    exit()

# Vérifier que les colonnes nécessaires existent
required_columns = ['source_de_verification', 'lien_vers_verification', 'Langue']
if not all(col in df.columns for col in required_columns):
    missing_cols = [col for col in required_columns if col not in df.columns]
    raise ValueError(f"Le fichier Excel doit contenir les colonnes : {', '.join(missing_cols)}")

# Fonction pour déterminer la langue
def determine_language(row):
    langue = row['Langue']
    source = row['source_de_verification']
    lien = row['lien_vers_verification']
    
    # Si la langue est déjà spécifiée, standardiser
    if isinstance(langue, str):
        langue = langue.lower()
        if langue in ['français', 'fr', 'francais']:
            return 'FR'
        if langue in ['anglais', 'ang', 'english']:
            return 'ANG'
    
    # Liste des sources francophones
    francophone_sources = [
        'TVA Nouvelles', 'Journal de Montréal', 'Journal de Québec', 'La Presse', 
        'Agence Science-Presse', 'Radio-Canada', 'Le Devoir', 'Le Nouvelliste', 
        'Vingt55', 'Viva Média', 'EnBeauce', 'Journal La Tribune', 
        'Conseil canadien pour les réfugiés', 'Espace pour la vie', 
        'Ministère de l’Éducation du Québec', 'Élections Québec', 
        'Service de Police de Gatineau', 'IRIS', 'Courrier Laval' , 'AFP Factuel' , 'Facebook'

    ]
    
    # Liste des sources anglophones
    anglophone_sources = [
        'FactCheck.org', 'The Guardian', 'Associated Press', 'Global News', 
        'Media Ecosystem Observatory', 'Cult MTL', 'NewsGuard', 'HuffPost', 
        'Reuters Fact Check', 'BBC Afrique'
    ]
    
    # Vérification basée sur la source
    if isinstance(source, str):
        if source in francophone_sources or 'Document universitaire' in source:
            return 'FR'
        if source in anglophone_sources:
            return 'ANG'
        if source == 'N' or source == 'Aucun':
            return 'N'
    
    # Vérification basée sur le lien
    if isinstance(lien, str):
        if any(x in lien.lower() for x in ['.qc.ca', '.ca/fr', 'fr.', 'français', 'francais']):
            return 'FR'
        if any(x in lien.lower() for x in ['.org', '.com', 'en.', 'english']):
            return 'ANG'
    
    # Par défaut, si aucune information claire
    return 'N'

# Appliquer la détermination de la langue à la colonne 'Langue'
df['Langue'] = df.apply(determine_language, axis=1)

# Exporter vers un nouveau fichier Excel
output_file = 'analyse_langue.xlsx'
df.to_excel(output_file, index=False, sheet_name='Données')

print(f"Fichier Excel '{output_file}' généré avec succès !")

# Afficher un aperçu des 10 premières lignes
print("\nAperçu des données (colonne Langue) :")
print(df[['source_de_verification', 'lien_vers_verification', 'Langue']].head(10))