import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurer le style des graphiques
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (12, 6)  # Taille ajustée pour clarté

# Créer un dossier pour sauvegarder les graphiques
output_dir = r"C:\Users\doghm\Desktop\projet-infox\graphiques\IA"
os.makedirs(output_dir, exist_ok=True)

# Chemin vers le fichier Excel
fichier_excel = r"C:\Users\doghm\Desktop\projet-infox\IA.xlsx"

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

# Extraire trimestre (YYYY-Q)
df['trimestre'] = df['date_de_repérage'].dt.to_period('Q').astype(str)
df['thématique'] = df['thématique'].str.strip()

# Regrouper les thématiques rares (moins de 5 infox) en "Autres"
theme_counts = df['thématique'].value_counts()
rares = theme_counts[theme_counts < 5].index
df['thématique_groupée'] = df['thématique'].apply(lambda x: 'Autres' if x in rares else x)

# 1. Barres empilées : Infox par thématique et trimestre
plt.figure()
pivot_table = df.pivot_table(index='trimestre', columns='thématique_groupée', aggfunc='size', fill_value=0)
pivot_table.plot(kind='bar', stacked=True, colormap='tab10')
plt.title("Nombre d'infox par thématique et trimestre")
plt.xlabel("Trimestre (Année-Trimestre)")
plt.ylabel("Nombre d'infox")
plt.legend(title="Thématique", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "thematique_trimestre_barres_empilees.png"))
plt.close()

# 2. Lignes multiples : Évolution par thématique
plt.figure()
for theme in df['thématique_groupée'].unique():
    theme_data = df[df['thématique_groupée'] == theme].groupby('trimestre').size()
    plt.plot(theme_data.index, theme_data.values, marker='o', label=theme)
plt.title("Évolution des infox par thématique par trimestre")
plt.xlabel("Trimestre (Année-Trimestre)")
plt.ylabel("Nombre d'infox")
plt.legend(title="Thématique", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "thematique_trimestre_lignes.png"))
plt.close()

print(f"\nGraphiques sauvegardés dans : {output_dir}")
print("Fichiers générés :")
print("- thematique_trimestre_barres_empilees.png")
print("- thematique_trimestre_lignes.png")