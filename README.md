# Courbes de service avec le Network Calculus

Ce dépôt présente le développement et l’implémentation de deux types de courbes de service dans le cadre du **Network Calculus**.

## Contexte

- **Network Calculus** : cadre mathématique permettant de modéliser et d’analyser les performances des systèmes réseaux en termes de délais, de débit et de ressources disponibles.  
- **Courbe de service** : fonction décrivant la capacité de service garantie qu’un système peut fournir à un flux de données.  

Deux types de courbes de service sont implémentées dans ce dépôt :  
- **Minimale**  
- **Stricte**

## Contenu du dépôt

Le projet est organisé autour de deux parties principales :

### 1. Extraction et préparation des données
`./Data_Extraction`  
- **`extraction.ipynb`** : notebook pour l’extraction des données. Il fournit :  
  - les détails de l’extraction,  
  - les paramètres à modifier pour effectuer différentes extractions,  
  - la génération des résultats dans un dossier `data_extracted` structuré en *mission/scénario*.  
- **`./data_extracted`** : résultats d’extraction produits par le notebook précédent.  
- **`./data_used`** : fichiers CSV bruts utilisés comme entrée.  
- **`./utils`** : code fourni par **KDbench** pour l’extraction.

### 2. Algorithmes des courbes de service
`./algorithmes/algos.ipynb`  
Ce notebook contient :  
- la préparation des données,  
- la visualisation des données extraites (fichier `../data_used`),  
- l’implémentation des algorithmes pour les courbes de service minimale et stricte,  
- leur application sur les données ainsi que la visualisation des résultats.  

Des paramètres sont personnalisables dans le notebook :  
- la tâche / mission / scénario (si les données correspondantes ont été extraites),  
- le taux de service **R**,  
- l’échantillonnage des données à visualiser.  

## Format du projet

Le code est fourni sous forme de **notebooks Jupyter**, afin de :  
- faciliter la compréhension des étapes (extraction, préparation, application),  
- proposer une exécution progressive et visualisable.  

## Références

Les données CSV brutes utilisées ainsi qu’une partie du code d’extraction (notamment `./Data_Extraction/utils`) proviennent du dépôt officiel **KDbench**, développé par l’équipe **Kopernic (Inria)** :  
https://gitlab.inria.fr/kdbench

---

<p align="center">
<sub><i>fait avec amour par ASHL</i></sub>
</p>
