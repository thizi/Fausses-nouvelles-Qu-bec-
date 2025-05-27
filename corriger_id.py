import pandas as pd

# Charger le fichier Excel
fichier_excel = "infox.xlsx"  
df = pd.read_excel(fichier_excel)

df['id'] = range(1, len(df) + 1)

# Enregistrer les modifications dans un nouveau fichier Excel
nouveau_fichier = "infox_corrige.xlsx"
df.to_excel(nouveau_fichier, index=False)

print(f"Le fichier '{nouveau_fichier}' a été créé avec les IDs numérotés.")