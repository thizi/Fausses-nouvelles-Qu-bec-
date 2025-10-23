
# 🇨🇦 French Fake News Corpus – Québec & Canada

Bonjour ! 👋  
Merci d’utiliser notre corpus francophone sur la désinformation au Québec et au Canada.

---

##  Structure du dépôt

Le dépôt contient plusieurs dossiers correspondant aux différentes composantes du corpus :

### **textes complets/**
Contient les articles intégraux, tels qu’ils ont été collectés à partir des sites web et plateformes sociales.  
Ce dossier est divisé en quatre sous-dossiers :

- `faux/` : contient les textes des fausses nouvelles ;  
- `vrai/` : contient les textes des vraies nouvelles ;  
- `fausses méta-informations/` : contient les métadonnées associées à chaque fausse nouvelle ;  
- `vraies méta-informations/` : contient les métadonnées associées à chaque vraie nouvelle.

---

###  **AI généré/**
Ce dossier contient des **fausses nouvelles générées par intelligence artificielle**.  
Il comprend **deux sous-dossiers distincts**, correspondant à deux processus de génération :

#### 1. **RealToFake/**
> Ce sont des **fausses nouvelles générées par l’IA à partir de vraies nouvelles**.

Chaque sous-dossier contient :
- `fake/` : les textes générés automatiquement par l’IA à partir d’articles réels ;  
- `fake-meta-information/` : les métadonnées associées à chaque texte généré (ID, texte synthétique, modifications appliquées).

#### 2. **FakeToEnhanceFake/**
> Ce sont des **fausses nouvelles initialement générées par l’IA, puis améliorées (« enhanced ») par une autre IA** afin de produire des versions plus réalistes.

Chaque sous-dossier contient :
- `fake/` : les textes retravaillés par l’IA pour paraître plus crédibles ;  
- `fake-meta-information/` : les métadonnées détaillant les changements et le processus d’amélioration.


##  Contenu des fichiers de métadonnées

Les fichiers présents dans les dossiers **fausses méta-informations**, **vraies méta-informations**, et **AI généré/** suivent une structure tabulaire (une ligne par champ).  
Chaque fichier correspond à une seule nouvelle et contient les champs suivants :

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

---


## Objectif du corpus

Ce corpus a été conçu dans le cadre d’un projet universitaire visant à :
- Étudier la désinformation francophone au Canada et au Québec ;  
- Fournir une base de données riche et annotée pour la recherche en traitement automatique du langage (TAL/NLP) ;  
- Offrir une ressource réutilisable pour la formation de modèles de détection automatique des fausses nouvelles.



## Format et utilisation

Les fichiers sont fournis en format `.txt` pour faciliter l’importation dans des outils d’analyse de texte (Python,Excel, etc.) 
Chaque ligne représente une nouvelle, avec ses métadonnées complètes.




> GitHub Repository: https://github.com/thizi/Fausses-nouvelles-Qu-bec-


Merci d’avoir consulté notre travail !  
