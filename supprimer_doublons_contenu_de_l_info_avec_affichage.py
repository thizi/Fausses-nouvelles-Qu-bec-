import pandas as pd

# Fonction pour normaliser le texte (ignorer casse et espaces)
def normaliser_texte(texte):
    if pd.isna(texte):
        return ""
    return ' '.join(str(texte).strip().lower().split())

# Charger les données (remplace par ton fichier Excel ou CSV)
fichier_excel = "infox_sources_nommees_corrigees.xlsx"  # À modifier
try:
    df = pd.read_excel(fichier_excel)
    print("Colonnes dans le fichier :", df.columns.tolist())
except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_excel}' n'a pas été trouvé.")
    exit()

# Vérifier si la colonne 'contenu_de_l_info' existe
if 'contenu_de_l_info' not in df.columns:
    print("Erreur : La colonne 'contenu_de_l_info' n'existe pas dans le fichier.")
    exit()

# Afficher le nombre d'entrées avant suppression
print(f"\nNombre d'entrées avant suppression des doublons : {len(df)}")

# Normaliser les entrées pour détecter les doublons
df['contenu_normalise'] = df['contenu_de_l_info'].apply(normaliser_texte)

# Identifier les doublons
doublons = df[df['contenu_normalise'].duplicated(keep='first')]

# Afficher les doublons trouvés et supprimés
if not doublons.empty:
    print("\nDoublons trouvés et supprimés :")
    for index, row in doublons.iterrows():
        print(f"- {row['contenu_de_l_info']}")
else:
    print("\nAucun doublon trouvé.")

# Supprimer les doublons basés sur la colonne normalisée (conserver la première occurrence)
df_sans_doublons = df.drop_duplicates(subset='contenu_normalise', keep='first')

# Supprimer la colonne temporaire
df_sans_doublons = df_sans_doublons.drop(columns=['contenu_normalise'])

# Afficher le nombre d'entrées après suppression
print(f"\nNombre d'entrées après suppression des doublons : {len(df_sans_doublons)}")

# Enregistrer dans un nouveau fichier
nouveau_fichier = "infox_contenu_sans_doublons.xlsx"
df_sans_doublons.to_excel(nouveau_fichier, index=False)
print(f"\nFichier '{nouveau_fichier}' créé avec les doublons supprimés.")