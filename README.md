# README — Service Curve Learning

### 1. Data_Extraction/
Contient le notebook d’extraction des données (activations, fins, xtimes) pour les 9 tâches dans différents missions/scénarios.  
- utils/ : code fourni par KDBench pour l’extraction  
- data_used/ : fichiers CSV bruts utilisés comme entrée  
- data_extracted/ (généré automatiquement) : résultats structurés par mission/scénario, sous forme de CSV

### 2. algorithmes/
Contient un notebook avec :  
- la visualisation des données extraites  
- l’implémentation des algorithmes d’apprentissage des courbes de service  
- des applications sur les données issues de l’extraction
