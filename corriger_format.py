import pandas as pd

# Fonction pour standardiser les formats
def standardiser_format(format_str):
    # Convertir en chaîne et nettoyer
    format_str = str(format_str).strip().lower().replace("/ ", "/").replace(" /", "/").replace("+", "/").replace(" ,", ",")
    
    # Corriger les erreurs typographiques
    if format_str == "texe":
        format_str = "texte"
    if format_str == "video":
        format_str = "vidéo"
    
    # Dictionnaire de regroupement
    categories = {
        "Texte": ["texte", "publication texte", "article", "article en ligne", "texte (post)", "texte (blog)", 
                  "communiqué", "texte viral", "tweet d’actualité", "texte (courriel)", "article/vidéo", 
                  "article web/textuel", "texte/images", "texte/image"],
        "Vidéo": ["vidéo", "video", "vidéo truquée", "vidéo virale", "vidéo/news et posts", "vidéo/texte", 
                  "vidéo/caption", "texte/vidéos", "article vidéo / texte", "vidéo / récit"],
        "Image": ["image", "image/texte", "texte (+photos)", "texte/image", "texte+image", "image+texte"],
        "Audio": ["audio", "audio/vidéo", "message audio", "audio/reportage"],
        "Publication sur réseau social": ["publication sur réseau social", "publication sur réseaux sociaux", 
                                        "tweet viral", "texte/image sur réseaux sociaux"],
        "Article satirique": ["article satirique"],
        "Publicité": ["publicité"],
        "Déclaration orale": ["déclaration orale", "annonce"],
        "Autres": ["appel téléphonique", "message texte sur app de messagerie", "canada/mondial", 
                   "publications texte/images, vidéos", "vidéo/texte, infographies mensongères", 
                   "posts, vidéos deepfake, faux sites d’info"]
    }
    
    # Diviser les formats si plusieurs sont listés
    formats_liste = [f.strip() for f in format_str.split("/")]
    
    # Vérifier la première catégorie correspondante
    for format in formats_liste:
        for categorie, termes in categories.items():
            if any(terme in format for terme in termes):
                return categorie
    
    # Si aucun format ne correspond, retourner "Autres"
    return "Autres"

# Charger le fichier Excel
fichier_excel = "infox_zones_corrigees.xlsx"
try:
    df = pd.read_excel(fichier_excel)
    print("Colonnes dans le fichier :", df.columns.tolist())
except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_excel}' n'a pas été trouvé.")
    exit()

# Vérifier si la colonne 'format' existe
if 'format' not in df.columns:
    print("Erreur : La colonne 'format' n'existe pas dans le fichier.")
    exit()

# Afficher quelques valeurs avant transformation
print("\nExemples de formats avant transformation :")
print(df['format'].head(10).to_list())

# Appliquer la fonction
df['format'] = df['format'].apply(standardiser_format)

# Afficher quelques valeurs après transformation
print("\nExemples de formats après transformation :")
print(df['format'].head(10).to_list())

# Enregistrer dans un nouveau fichier
nouveau_fichier = "infox_formats_corriges.xlsx"
df.to_excel(nouveau_fichier, index=False)
print(f"\nFichier '{nouveau_fichier}' créé avec les formats corrigés.")