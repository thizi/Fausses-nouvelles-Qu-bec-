import pandas as pd

# Fonction pour standardiser les plateformes de diffusion
def standardiser_plateforme_diffusion(plateforme):
    # Convertir en chaîne et nettoyer
    plateforme = str(plateforme).strip().lower().replace("/", ", ").replace(" ,", ",").replace(", ", ",").replace(" , ", ",")
    
    # Gérer "Non spécifiée"
    if plateforme in ["non spécifiée", "non specifiée"]:
        return "Autres"
    
    # Dictionnaire de regroupement
    categories = {
        "Facebook": ["facebook", "facebook (post)", "facebook (sponsored ad)", "facebook ads", 
                     "facebook/internet", "facebook/pages politiques"],
        "YouTube": ["youtube", "youtube/facebook", "youtube, facebook"],
        "Twitter/X": ["twitter", "x (twitter)", "twitter/x", "x", "twitter (x)"],
        "TikTok": ["tiktok", "tiktok/instagram"],
        "Instagram": ["instagram"],
        "WhatsApp": ["whatsapp", "whatsapp, facebook"],
        "Telegram": ["telegram"],
        "Reddit": ["reddit"],
        "Blogs/Forums": ["blogs", "forums", "blog internet", "blogs conspirationnistes", "forums en ligne", 
                         "blogs/forums", "blog/forum", "blog satirique", "blog personnel"],
        "Médias traditionnels": ["radio locale", "journal de montréal", "la presse", "radio-canada", "huffpost", 
                                "sciencepresse", "débats électoraux", "débats télévisés", "télévisions locales"],
        "Courriel": ["courriel", "courriel/facebook", "courriel / publicité fb"],
        "Autres": ["site web viral", "appels téléphoniques", "rumeurs locales", "messages instantanés", 
                   "vidéo publicitaire en ligne", "spotify", "snapchat", "médias non vérifiés"]
    }
    
    # Diviser les plateformes si plusieurs sont listées
    plateformes_liste = [p.strip() for p in plateforme.split(",")]
    
    # Vérifier la première plateforme dans la liste
    for plateforme in plateformes_liste:
        for categorie, termes in categories.items():
            if any(terme in plateforme for terme in termes):
                return categorie
    
    # Si aucune plateforme ne correspond, retourner "Autres"
    return "Autres"

# Charger le fichier Excel
fichier_excel = "infox_public_cible_corrige.xlsx"
try:
    df = pd.read_excel(fichier_excel)
    print("Colonnes dans le fichier :", df.columns.tolist())
except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_excel}' n'a pas été trouvé.")
    exit()

# Vérifier si la colonne 'plateforme_de_diffusion' existe
if 'plateforme_de_diffusion' not in df.columns:
    print("Erreur : La colonne 'plateforme_de_diffusion' n'existe pas dans le fichier.")
    exit()

# Afficher quelques valeurs avant transformation
print("\nExemples de plateformes avant transformation :")
print(df['plateforme_de_diffusion'].head(10).to_list())

# Appliquer la fonction
df['plateforme_de_diffusion'] = df['plateforme_de_diffusion'].apply(standardiser_plateforme_diffusion)

# Afficher quelques valeurs après transformation
print("\nExemples de plateformes après transformation :")
print(df['plateforme_de_diffusion'].head(10).to_list())

# Enregistrer dans un nouveau fichier
nouveau_fichier = "infox_plateformes_corrigees.xlsx"
df.to_excel(nouveau_fichier, index=False)
print(f"\nFichier '{nouveau_fichier}' créé avec les plateformes de diffusion corrigées.")