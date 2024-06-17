#!/usr/bin/python3

####################################################################################
##  Script de calcul du score aux olympiades
##  Se base sur https://docs.google.com/spreadsheets/d/1PV6gNqFVh0EgnfO3hGagLEsJ_QWj-7n3-DLuR_-kJdM/edit#gid=1502502214
##  Le calcul de score se fait par interpolation de la performance selon le fichier "bareme.csv" sauf pour les épreuves Ballons et Pétanque qui sont codées en dur.
####################################################################################

import pandas as pd
import numpy as np

## Paramètres
input_bareme_file = './data/bareme.csv'
input_resultats_file = './data/resultats.csv'     # Ce fichier est créé par copier-coller en csv (sep = ';') depuis https://docs.google.com/spreadsheets/d/1PV6gNqFVh0EgnfO3hGagLEsJ_QWj-7n3-DLuR_-kJdM/edit#gid=1502502214
output_scores_file = './data/scores.csv'
output_scores_equipes_file = './data/scores_equipes.csv'

epreuves = ['Cross', 'Natation', 'Sprint', 'Poids', 'Ballons', 'Pétanque']
colonnes_indiv = ['Classement', 'Participant', 'Genre', 'Équipe', 'Cross', 'Score Cross', 'Natation', 'Score Natation','Sprint', 'Score Sprint', 'Poids', 'Score Poids', 'Ballons', 'Score Ballons','Pétanque', 'Score Pétanque', 'Score Total']

## Fonctions
def convert_time_to_seconds(time_str):
    '''Convertit un temps mm:ss en secondes'''
    try:
        minutes, seconds = time_str.split(':')
        return int(minutes) * 60 + int(seconds.replace(',', '.'))
    except ValueError:
        return None

def convert_str_to_float(str):
    '''Convertit une chaine de caractères en float'''
    return float(str.replace(',', '.'))

def calculate_score(perf, epreuve, df):
    '''Calcule du score sur 1000 selon la performance sur l'épreuve'''
    if not perf:
        return None

    if epreuve not in epreuves:
        raise ValueError(f"L'épreuve '{epreuve}' n'existe pas")

    if epreuve in ['Cross', 'Natation']:
        perf = convert_time_to_seconds(perf)
    else:
        try:
            perf = float(perf.replace(',', '.'))
        except:
            perf = float(perf)

    # Calcul du score
    if epreuve in ['Poids']:
        # np.interp nécessite que la série soit croissante, ce qui n'est pas le cas de df["Poids"] 
        interpolated_scores = round(np.interp(perf, df[epreuve][::-1], df['Scores'][::-1]))
    elif epreuve in ['Ballons', 'Pétanque']:
        # calcul en dur du score pétanque ballons : 40 points pour les 10 premiers marqués, 30 points ensuite
        interpolated_scores = round((perf > 10) * (40 * 10 + (perf-10) * 30) + (perf <= 10) * perf * 40)
    else:
        # interpolation pour le reste
        interpolated_scores = round(np.interp(perf, df[epreuve], df['Scores']))

    return interpolated_scores

def calculate_team_score(group, epreuve):
    '''Calcule du score sur une épreuve pour une équipe'''

    # Suppression des participants qui n'ont pas fait l'épreuve
    group = group.dropna(subset=[epreuve])

    # On garde le meilleur score pour chaque genre
    scores_h, scores_f = group[group['Genre'] == 'M'][epreuve], group[group['Genre'] == 'F'][epreuve]
    try:
        score_max_h, id_max_h = scores_h.max(), scores_h.idxmax()
    except:
        score_max_h, id_max_h = 0, np.nan
    try:
        score_max_f, id_max_f = scores_f.max(), scores_f.idxmax()
    except:
        score_max_f, id_max_f = 0, np.nan
    idmax = [id for id in [id_max_h, id_max_f] if id is not np.nan] # on enlève les NaN : si pas de genre dans l'épreuve, pas de points

    # On identifie les deux meilleurs résultats sur les participants moins le meilleur homme et femme
    two_best_scores = group.drop(idmax).sort_values(epreuve, ascending=False)[epreuve].head(2)
    two_best_scores = [best_score for best_score in two_best_scores if best_score is not np.nan]    # on enlève les NaN : si moins de 4 participants, moins de points
    
    # On calcule le score total
    score_total = int(score_max_f + score_max_h + sum(two_best_scores))
    
    return score_total


################
##    MAIN    ##
################
if __name__ == '__main__':
    # Lecture des fichiers en entrée
    converters = {
        'Cross': convert_time_to_seconds,
        'Natation': convert_time_to_seconds,
        'Sprint': convert_str_to_float,
        'Poids': convert_str_to_float
    }
    bareme = pd.read_csv(input_bareme_file, sep=';', decimal=',', converters=converters)
    resultats = pd.read_csv(input_resultats_file, sep=';', decimal=',', keep_default_na = False)

    # Calcul des scores individuels + écriture du csv de sortie
    for epreuve in epreuves:
        resultats[f'Score {epreuve}'] = resultats.apply(lambda row: calculate_score(row[epreuve], epreuve, bareme), axis=1)
    resultats['Score Total'] = resultats.filter(like='Score').sum(axis=1)   # somme des colonnes contenant le mot "Score"
    resultats = resultats.sort_values(by='Score Total', ascending=False)
    resultats['Classement'] = range(1, len(resultats) + 1)
    resultats = resultats[colonnes_indiv]
    resultats.to_csv(output_scores_file, index=False)

    # Calcul des scores par équipe + écriture du csv de sortie
    resultats_equipe = pd.DataFrame(
        index = resultats['Équipe'].unique(),
        columns = ['Équipe'] + epreuves + ['Score Total']
    )
    resultats_equipe['Équipe'] = resultats_equipe.index
    for epreuve in epreuves:
        resultats_equipe[epreuve] = resultats.groupby('Équipe').apply(calculate_team_score, f'Score {epreuve}')
    resultats_equipe['Score Total'] = resultats_equipe.drop('Équipe', axis=1).sum(axis=1)
    resultats_equipe.to_csv(output_scores_equipes_file, index=False)
