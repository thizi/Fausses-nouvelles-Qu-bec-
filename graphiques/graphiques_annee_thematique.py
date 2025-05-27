import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Configurer le style des graphiques
sns.set(style="whitegrid")
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (10, 6)

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

# Nettoyer impact_estimé (standardiser en catégories)
def nettoyer_impact(impact):
    if not isinstance(impact, str):
        return 'Inconnu'
    impact = impact.strip().lower()
    if 'élevé' in impact:
        return 'Élevé'
    elif 'modéré' in impact:
        return 'Modéré'
    elif 'faible' in impact:
        return 'Faible'
    return 'Inconnu'

df['impact_estimé_clean'] = df['impact_estimé'].apply(nettoyer_impact)

# Convertir date_de_repérage en datetime
df['date_de_repérage'] = pd.to_datetime(df['date_de_repérage'], format='%d/%m/%Y', errors='coerce')
df['annee_mois'] = df['date_de_repérage'].dt.to_period('M')

# 1. Histogramme : Type d'infox
plt.figure()
sns.countplot(data=df, x='type_d_infox', order=df['type_d_infox'].value_counts().index)
plt.title("Nombre d'infox par type")
plt.xlabel("Type d'infox")
plt.ylabel("Nombre")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "type_infox_histogramme.png"))
plt.close()

# 2. Histogramme : Thématique
plt.figure()
sns.countplot(data=df, x='thématique', order=df['thématique'].value_counts().index)
plt.title("Nombre d'infox par thématique")
plt.xlabel("Thématique")
plt.ylabel("Nombre")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "thematique_histogramme.png"))
plt.close()

# 3. Diagramme en donut : Impact estimé
impact_counts = df['impact_estimé_clean'].value_counts()
plt.figure()
plt.pie(impact_counts, labels=impact_counts.index, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
plt.title("Répartition des infox par impact estimé")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "impact_estime_donut.png"))
plt.close()

# 4. Histogramme : Plateforme de diffusion
plt.figure()
sns.countplot(data=df, x='plateforme_de_diffusion', order=df['plateforme_de_diffusion'].value_counts().index)
plt.title("Nombre d'infox par plateforme de diffusion")
plt.xlabel("Plateforme")
plt.ylabel("Nombre")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "plateforme_histogramme.png"))
plt.close()

# 5. Série temporelle : Infox par mois
plt.figure()
df['annee_mois'].value_counts().sort_index().plot(kind='line', marker='o')
plt.title("Évolution des infox par mois")
plt.xlabel("Année-Mois")
plt.ylabel("Nombre d'infox")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "evolution_temporelle.png"))
plt.close()

# 6. Histogramme : Public cible
plt.figure()
sns.countplot(data=df, x='public_cible', order=df['public_cible'].value_counts().index)
plt.title("Nombre d'infox par public cible")
plt.xlabel("Public cible")
plt.ylabel("Nombre")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "public_cible_histogramme.png"))
plt.close()

# 7. Diagramme en donut : Format
format_counts = df['format'].value_counts()
plt.figure()
plt.pie(format_counts, labels=format_counts.index, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
plt.title("Répartition des infox par format")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "format_donut.png"))
plt.close()

# 8. Heatmap : Thématique vs Impact estimé
pivot_table = df.pivot_table(index='thématique', columns='impact_estimé_clean', aggfunc='size', fill_value=0)
plt.figure()
sns.heatmap(pivot_table, annot=True, fmt='d', cmap='Blues')
plt.title("Nombre d'infox par thématique et impact estimé")
plt.xlabel("Impact estimé")
plt.ylabel("Thématique")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "thematique_impact_heatmap.png"))
plt.close()

print(f"\nGraphiques sauvegardés dans : {output_dir}")