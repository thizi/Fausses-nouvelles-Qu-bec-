import pandas as pd
import re

# Chemin vers le fichier Excel
file_path = 'infox_sources_nommees_corrigees.xlsx'

# Lire le fichier Excel
# Remplacez 'Sheet1' par le nom de la feuille si nécessaire
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Vérifier que la colonne 'impact_estimé' existe
if 'impact_estimé' not in df.columns:
    raise ValueError("Le fichier Excel doit contenir la colonne 'impact_estimé'")

# Fonction pour parser les vues/partages en valeurs numériques
def parse_views_shares(text):
    if not isinstance(text, str):
        return None
    text = text.lower().replace(" ", "").replace(" ", "")
    if any(x in text for x in ["nonprécisées", "inconnu", "victimes", "signalements", "avertissements"]):
        return None
    match = re.search(r'(\+?\d+\.?\d*[mMkK]?)\s*(vues|partages|écoutes|commentaires)', text)
    if match:
        value = match.group(1)
        if 'm' in value.lower():
            return int(float(value.replace('+', '').replace('m', '')) * 1_000_000)
        elif 'k' in value.lower():
            return int(float(value.replace('+', '').replace('k', '')) * 1_000)
        return int(value.replace('+', ''))
    if "milliers" in text:
        return 1000  # Estimation conservatrice pour "milliers de vues/partages"
    return None

# Fonction pour estimer/standardiser l'impact
def estimate_impact(text):
    if not isinstance(text, str):
        return 'N'  # Non précisé pour les valeurs non valides
    text = text.lower()
    
    # Si l'impact est déjà classé, standardiser
    if text in ['faible', 'modéré', 'élevé', 'moyen']:
        return text.replace('moyen', 'Modéré').capitalize()
    
    # Parser la valeur numérique
    value = parse_views_shares(text)
    
    # Estimation basée sur le texte
    if any(x in text for x in ['très viral', 'plusieurs millions', 'grande échelle', 'largement partagé']):
        return 'Élevé'
    if any(x in text for x in ['circulé', 'localement', 'sporadique']):
        return 'Faible'
    if any(x in text for x in ['nonprécisées', 'inconnu', 'victimes', 'signalements', 'avertissements', 'démenti', 'explication']):
        return 'N'
    
    # Estimation basée sur la valeur numérique
    if value is None:
        return 'N'  # Non précisé pour les cas non quantifiables
    if value > 500_000:
        return 'Élevé'
    elif value >= 50_000:
        return 'Modéré'
    else:
        return 'Faible'

# Appliquer l'estimation/standardisation à la colonne 'impact_estimé'
df['impact_estimé'] = df['impact_estimé'].apply(estimate_impact)

# Exporter vers un nouveau fichier Excel
output_file = 'analyse_impact_simplifiee.xlsx'
df.to_excel(output_file, index=False, sheet_name='Données')

print(f"Fichier Excel '{output_file}' généré avec succès !")

# Afficher un aperçu des 10 premières lignes
print("\nAperçu des données :")
print(df[['impact_estimé']].head(10))