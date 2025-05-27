import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurer le style des graphiques
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (14, 8)  # Taille plus grande pour la heatmap

# Créer un dossier pour sauvegarder les graphiques
output_dir = r"C:\Users\doghm\Desktop\projet-infox\graphiques"
os.makedirs(output_dir, exist_ok=True)

# Chemin vers le fichier Excel
fichier_excel = r"C:\Users\doghm\Desktop\projet-infox\analyse_langue.xlsx"

# Charger le fichier Excel
try:
    df = pd.read_excel(fichier_excel)
    print("Fichier chargé avec succès.")
    print("Colonnes disponibles :", df.columns.tolist())
except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_excel}' n'a pas été trouvé. Vérifie le chemin.")
    exit()
except Exception as e:
    print(f"Erreur lors du chargement du fichier : {e}")
    exit()

# Convertir date_de_repérage en datetime
df['date_de_repérage'] = pd.to_datetime(df['date_de_repérage'], format='%d/%m/%Y', errors='coerce')

# Vérifier les données manquantes
if df['date_de_repérage'].isna().any():
    print(f"Avertissement : {df['date_de_repérage'].isna().sum()} entrées avec date invalide, ignorées.")
    df = df.dropna(subset=['date_de_repérage'])

# Extraire année et mois
df['année_mois'] = df['date_de_repérage'].dt.to_period('M').astype(str)  # Format "YYYY-MM"
df['thématique'] = df['thématique'].str.strip()  # Nettoyer thématique

# Créer une table pivot pour la heatmap
pivot_table = df.pivot_table(index='thématique', columns='année_mois', aggfunc='size', fill_value=0)

# Générer la heatmap
plt.figure()
sns.heatmap(pivot_table, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': "Nombre d'infox"})
plt.title("Nombre d'infox par thématique et mois (Année-Mois)")
plt.xlabel("Année-Mois")
plt.ylabel("Thématique")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "thematique_annee_mois_heatmap.png"))
plt.close()

print(f"\nGraphique sauvegardé dans : {output_dir}\thematique_annee_mois_heatmap.png")