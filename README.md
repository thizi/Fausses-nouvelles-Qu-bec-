
## 🇨🇦 French Fake News Corpus – Quebec & Canada

Bonjour ! 👋  
Merci d’utiliser notre corpus francophone sur la désinformation au Québec et au Canada.


##  Structure du dépôt

Le dépôt contient un dossier qui correspond aux différentes composantes du corpus :

- **textes complets/**  
  Contient les articles intégraux, tels qu’ils ont été collectés à partir des sites web et plateformes sociales.  
  Ce dossier est divisé en quatre sous-dossiers :
  - `faux/` : contient les textes des fausses nouvelles ;
  - `vrai/` : contient les textes des vraies nouvelles ;
  - `fausses méta-informations/` : contient les métadonnées associées à chaque fausse nouvelle ;
  - `vraies méta-informations/` : contient les métadonnées associées à chaque vraie nouvelle.


## 🧾 Contenu des fichiers de métadonnées

Les fichiers présents dans les dossiers **fausses méta-informations** et **vraies méta-informations** suivent une structure tabulaire (une ligne par champ).  
Chaque fichier correspond à une seule nouvelle (fausse ou vraie) et contient les champs suivants :

id  
date_de_repérage  
contenu_de_l_info  
type_d_infox  
thématique  
objectif_possible  
public_cible  
plateforme_de_diffusion  
zone_geographique  
format  
véracité  
source_de_verification  
lien_vers_verification  
impact_estimé  
Langue



## Objectif du corpus

Ce corpus a été conçu dans le cadre d’un projet universitaire visant à :
- Étudier la désinformation francophone au Canada et au Québec ;  
- Fournir une base de données riche et annotée pour la recherche en traitement automatique du langage (TAL/NLP) ;  
- Offrir une ressource réutilisable pour la formation de modèles de détection automatique des fausses nouvelles.


## Format et utilisation

Les fichiers sont fournis en format `.csv` ou `.txt` pour faciliter l’importation dans des outils d’analyse de texte (Python,Excel etc.).  
Chaque ligne représente une nouvelle, avec ses métadonnées complètes.



> GitHub Repository: https://github.com/thizi/Fausses-nouvelles-Qu-bec-


Merci d’avoir consulté notre travail !  
