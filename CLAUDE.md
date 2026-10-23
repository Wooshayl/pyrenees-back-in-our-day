# Projet : « Courir en Ariège, hier et aujourd'hui » — dashboard Streamlit

Projet individuel EFREI (Data Visualisation, 2026) : app Streamlit de *data storytelling*
sur des données ouvertes. Le sujet complet est dans le PDF de consignes (à mettre dans ce dossier).

## Exigences du sujet (à respecter)
- Narration : accroche → contexte → insights → implications. Une phrase-titre par section.
- Barre latérale avec filtres (dates, stations/départements, variable).
- ≥ 3 visuels interactifs (Plotly, infobulles), au moins une carte (les stations ont lat/lon).
- Rangée de KPI liée aux filtres.
- Section qualité des données : valeurs manquantes, doublons, contrôles de validité.
- Performance : `st.cache_data`, pré-agrégation (8,8 M lignes brutes → agrégats annuels/mensuels en parquet).
- Accessibilité : axes et unités étiquetés, couleurs lisibles (palette daltonien-friendly), texte alternatif sous chaque graphique.
- Reproductibilité : `requirements.txt`, README avec instructions, script de téléchargement des données.
- Streamlit ≥ 1.33. Structure conseillée : `app.py`, `sections/` (intro, overview, deep_dives, conclusions), `utils/` (io, prep, viz), `data/`.

## Données
- Source : Météo-France, « Données climatologiques de base — quotidiennes »,
  https://www.data.gouv.fr/datasets/6569b51ae64326786e4e8e1a — Licence Ouverte 2.0.
- Téléchargement : `python download_data.py` (⚠ fichier supprimé, à recréer) (API data.gouv.fr, ne retélécharge pas l'existant,
  `--force` pour rafraîchir). Ne pas committer `data/raw/` : l'app doit fonctionner après ce script.
- Fichiers dans `data/raw/` : 5 départements pyrénéens (09, 31, 64, 65, 66) × 4 fichiers :
  `Q_XX_previous-1950-2024_RR-T-Vent.csv.gz`, `Q_XX_latest-2025-2026_RR-T-Vent.csv.gz`,
  `Q_XX_previous-1950-2024_autres-parametres.csv.gz`, `Q_XX_latest-2025-2026_autres-parametres.csv.gz`.
- Format : CSV séparateur `;`, gzip. Une ligne = une station × un jour (`AAAAMMJJ`).
  Identifiant station `NUM_POSTE` (8 caractères, les 2 premiers = département — lire en texte).
  Métadonnées : `NOM_USUEL`, `LAT`, `LON`, `ALTI`.
- Variables utiles : `TX`/`TN` (températures max/min, °C), `RR` (pluie, mm),
  `NEIGETOTX` (hauteur de neige max, cm), `HNEIGEF` (neige fraîche, cm).
  Chaque variable a un code qualité `Q<variable>`.
- Les fichiers RR-T-Vent et autres-paramètres couvrent les mêmes jours avec des colonnes différentes.

## Ce que le test de viabilité a montré (`check_viability.py`, `data/station_inventory.csv`)
- 597 stations, dont 308 avec au moins une année complète de température.
- 37 longues séries de température (début ≤ 1960, ≥ 40 années complètes), dont 8 au-dessus de 1000 m.
- Ariège : St Girons (414 m, 1950–2026) et Ascou Lavail (1090 m, 1959–2026) toujours actives →
  comparaison vallée / montagne possible. Pic du Midi (2880 m) actif depuis 1950.
- Neige : 21 stations avec ≥ 20 ans de données ; Aulus-les-Bains 54 ans, Hospitalet 41 ans.
- Premiers chiffres (années ≥ 330 jours renseignés) : tendance TX ≈ +0,3 à +0,45 °C/décennie ;
  St Girons : jours ≥ 30 °C passés de ~12/an (1961-1990) à ~25/an (depuis 2011).
- Anomalie à expliquer : Aulus-les-Bains montre PLUS de jours de gel récemment (73 → 96) —
  probable changement de site/capteur. Exemple concret du problème d'homogénéisation.

## Histoire de l'app (validée le 2026-10-20) — tout le texte de l'app en anglais
Titre : *"Back in our day…": have the Pyrenees really changed?* Chaque chapitre part d'une phrase
des grands-parents, la confronte aux relevés, et donne un verdict : True / Partly true / False / Can't tell.
- Prologue (`sections/intro.py`) : accroche (courir sur les sentiers ariégeois) + rangée de KPI liée aux filtres.
- Ch.1 « The witnesses » : carte des stations + interaction année de naissance d'un grand-parent
  (ses 20 ans vs les 10 dernières années complètes 2016-2025 ; année de naissance ~1930-1980).
- Ch.2 « Summers weren't this hot » : jours ≥ 30 °C. St Girons 11,8 → 24,4/an → True.
- Ch.3 « Winters were harsher » : jours de gel. Aulus 73 → 96 (station s'arrête en 2018, changement de site probable) → Partly true.
- Interlude « Can we trust the thermometers? » : section qualité obligatoire (manquants, doublons, contrôles).
- Ch.4 « There was more snow » : aucune station de montagne ne couvre 1960→aujourd'hui (anciennes séries
  arrêtées 1984-2016, nivoses automatiques depuis ~1998). Seule Ascou Lavail 1972-2023 : pas de tendance nette → Can't tell.
- Ch.5 « At least it's cooler in the mountains » : Ascou +0,45 °C/décennie vs St Girons +0,35 ; Pic du Midi TX moyenne
  1,5 → 3,2 °C (+1,7, autant que la vallée +1,8 ; tendance +0,28/décennie) → False.
- Ch.6 « So when should I run? » : sliders jour idéal (TX entre X et Y, pluie ≤ Z), par mois, années 1960 vs aujourd'hui
  (`witness_daily.csv`) → partie what-if.

## Structure de l'app (code volontairement très simple, niveau débutant Streamlit)
- `app.py` : la barre latérale = sommaire (`st.sidebar.radio`) + `if/elif` qui appelle `show()` du chapitre.
- `sections/` : un fichier par page (intro, chapter1_witnesses … chapter6_running, interlude_quality, conclusion).
  Les réglages (station, sliders) sont dans les pages, pas dans la barre latérale.
- `utils/io.py` : lecture des CSV avec `@st.cache_data` + dictionnaire `WITNESSES`.
- `utils/viz.py` : toutes les fonctions de graphiques Plotly (palette Okabe-Ito).
- Sous chaque graphique : `st.caption` = texte alternatif. Le texte de l'app sera retouché par l'utilisateur.

## Fichiers produits par `prepare_data.ipynb` (dans `data/processed/`, lire `station` en texte)
`stations.csv`, `yearly.csv`, `monthly.csv`, `winters.csv` (déc-mars), `quality_checks.csv`, `quality_missing.csv`, `witness_daily.csv` (5 stations témoins :
09289001 St Girons, 09023002 Ascou Lavail, 09029001 Aulus, 09139001 Hospitalet, 65059001 Pic du Midi).
Complétude : année valide si `days_tx` ≥ 330 ; hiver valide si `days_snow` ≥ 110.

## Limites à afficher dans l'app
- Données brutes, non homogénéisées (déplacements de stations, changements de capteurs).
  Référence possible : séries homogénéisées LSH, https://www.data.gouv.fr/datasets/6569b2c4f1937611d4c8b1a3
- Beaucoup de stations ouvrent/ferment : règles de complétude (année valide si ≥ 90 % des jours).
- Une tendance locale n'est pas une preuve sur le climat global ; pas de causalité sur-affirmée.

## Conventions de code
- Python, pandas, Plotly. Fonctions de graphiques centralisées dans `utils/viz.py`.
- Lire les identifiants en texte (`dtype=str`), ne charger que les colonnes utiles (`usecols`).
- Everything in English: code, comments, notebook text and app text.
