import pandas as pd

def standardiser_public_cible(public):
    # Convertir en chaîne et nettoyer
    public = str(public).strip().lower()
    
    categories = {
        "Grand public": ["grand public", "population générale", "public général", "citoyens", 
                         "internautes grand public", "public soucieux santé", "internautes curieux", 
                         "adultes, internautes", "populatiion peu informée", "voyageurs, population en général"],
        "Électeurs": ["électeurs", "électeurs canadiens", "électeurs québécois", "électeurs 60 ans et +", 
                      "électeurs de la classe moyenne", "électeurs préoccupés", "électeurs francophones", 
                      "sympathisants, électeurs", "électeurs, opposants", "électeurs, sceptiques"],
        "Antivaccins/Conspirationnistes": ["antivax", "anti-vaccins", "conspirationnistes anti-vaccin", 
                                          "internautes anti-vaccins", "sceptiques antivax", "anti-vaccins, lecteurs", 
                                          "internautes complotistes", "partisans de théories du complot", 
                                          "généralistes méfiants mesures sanitaires", "internautes anti-gouvernement", 
                                          "utilisateurs anti-masque et anti-vaccin", "internautes conspirationnistes, anti-israël"],
        "Jeunes": ["jeunes adultes", "jeunes internautes", "jeunes femmes", "jeunes utilisateurs de tinder", 
                   "jeunes adeptes de rencontres en ligne", "jeunes électeurs", "jeunes et adultes anti-vaccin"],
        "Parents": ["parents", "parents d’élèves", "parents, enseignants", "parents, communauté scolaire", 
                   "parents d’adolescents", "parents inquiets des vaccins", "parents, résidents", 
                   "parents, citoyens", "parents, familles"],
        "Internautes": ["internautes", "utilisateurs de tiktok", "utilisateurs de réseaux sociaux", 
                       "utilisateurs de facebook", "utilisateurs de youtube", "internautes, joueurs", 
                       "internautes, militants", "internautes de groupes conspi", "internautes de droite", 
                       "internautes, opposants politiques", "internautes, adversaires politiques"],
        "Seniors": ["personnes âgées", "électeurs seniors", "électeurs 60+", "électeurs âgés", 
                    "aidants naturels, seniors"],
        "Communautés spécifiques": ["communauté musulmane", "diaspora haïtienne", "communautés autochtones", 
                                   "communauté de montréal-nord", "musulmans/québécois", "bilingues, indépendantistes", 
                                   "adhérents au mouvement souverainiste", "communauté locale, parents"],
        "Consommateurs/Investisseurs": ["consommateurs", "consommateurs québécois", "investisseurs", 
                                       "investisseurs amateurs", "acheteurs en ligne", "clients sceptiques", 
                                       "consommateurs en ligne", "abonnés hydro-québec", "abonnés hydro"],
        "Résidents locaux": ["résidents", "résidents de montréal", "résidents de québec", "résidents de laval", 
                            "habitants de gatineau", "habitants de sherbrooke", "habitants de jonquière", 
                            "résidents de longueuil", "résidents de lévis", "résidents de saint-jérôme", 
                            "habitants de sept-îles", "résidents de drummondville", "résidents de blainville", 
                            "résidents de chicoutimi", "résidents de val-d'or", "résidents de saint-hyacinthe", 
                            "habitants, parents d’adolescents", "habitants de coteau-du-lac", "population locale"],
        "Autres": ["propriétaires d'animaux", "fans de l’animatrice", "admirateurs, grand public", 
                   "fans du cirque", "supporters de hockey", "fans de sports", "amateurs de science-fiction", 
                   "randonneurs, écologistes", "écologistes et complotistes", "amateurs d’oiseaux, citadins", 
                   "skieurs/touristes", "joueurs de loterie", "bénévoles, usagers", "cyclistes, randonneurs", 
                   "touristes, naturalistes", "voyageurs, automobilistes", "conducteurs, automobilistes", 
                   "grand public téléréalité", "militants pro-français", "personnes anti-écologie", 
                   "groupes nationalistes", "familles des résidents du chsld"]
    }
    
    # Vérifier à quelle catégorie appartient le public
    for categorie, termes in categories.items():
        if any(terme in public for terme in termes):
            return categorie
    
    # Par défaut, si aucun match, retourner "Autres"
    return "Autres"

# Charger le fichier Excel
fichier_excel = "infox_thematiques_corrigees.xlsx"
try:
    df = pd.read_excel(fichier_excel)
    print("Colonnes dans le fichier :", df.columns.tolist())
except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_excel}' n'a pas été trouvé.")
    exit()

# Vérifier si la colonne 'public_cible' existe
if 'public_cible' not in df.columns:
    print("Erreur : La colonne 'public_cible' n'existe pas dans le fichier.")
    exit()

# Afficher quelques valeurs avant transformation
print("\nExemples de public cible avant transformation :")
print(df['public_cible'].head(10).to_list())

# Appliquer la fonction
df['public_cible'] = df['public_cible'].apply(standardiser_public_cible)

# Afficher quelques valeurs après transformation
print("\nExemples de public cible après transformation :")
print(df['public_cible'].head(10).to_list())

# Enregistrer dans un nouveau fichier
nouveau_fichier = "infox_public_cible_corrige.xlsx"
df.to_excel(nouveau_fichier, index=False)
print(f"\nFichier '{nouveau_fichier}' créé avec les publics cibles corrigés.")