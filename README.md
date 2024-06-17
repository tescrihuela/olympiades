## Application web des Olympiades

Le calcul des scores se fait avec le script `compute_scores.py`, qui prend en entrée un csv contenant le barème et un csv contenant les résultats stockés [ici](https://docs.google.com/spreadsheets/d/1PV6gNqFVh0EgnfO3hGagLEsJ_QWj-7n3-DLuR_-kJdM/edit#gid=1502502214). Le script crée les csv `scores.csv` des scores individuels et `scores_equipes.csv` des scores par équipe.

L'application Dash est contenue dans `app.py` et utilise les csv des scores.
