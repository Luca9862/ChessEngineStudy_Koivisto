# tirocinio_lucacanali

## Repository structure:
- dataset
- engine
- shared_materials
- tools


### Dataset
- The dataset folder contains all the available research data: PGN files, CSV files, graphs and everything related to data and analysis

<figure>
  <img src="./images/table_ex.png" alt="example dataset">
  <figcaption>
    Example dataset from Banksia software
  </figcaption>
</figure>

### Engine
- The research within this repository concerns the study, analysis, improvement, and comparison with other chess engines by Koivisto.
- Official site: https://koivisto-chess.com
- Resource code: https://github.com/Luecx/Koivisto

### Shared materials

### Tools
- The tools folder contains all the scripts implemented for the research. In the following, they will be illustrated one by one.

### pgn_manager
- pgn_manager is a script implemented for the management of PGN files (merge, split, CSV creation, duplicate removal). The script has a very simple graphical interface consisting of 4 menus.
- create_csv allows you to write matches from a PGN file to a CSV dataset. In addition, appropriate checks are performed to avoid writing a duplicate match thanks to the SHA-256 algorithm, which allowed me to create unique keys for each match.
- INPUT ONE: pgn path (example: C:\users\u1\documents\matches.pgn)
- INPUT TWO: csv path where matches will be saved (example: C:\users\u1\desktop\dataset.csv) If csv don't exists the script creates it
<img src="./images/screen_pgnmanager1.png" alt="screen_gui" width = "320" height = "280">
- merge_pgn allows you to merge two PGN files. The merge will be performed in the second input file (destination pgn). All matches from the first file will be written to the second file.
- INPUT ONE: pgn file (example: C:\users\u1\documents\matches.pgn)
- INPUT TWO: pgn_file where the first file games will be saved (example: C:\users\u1\documents\matches.pgn)
<img src="./images/screen_pgnmanager2.png" alt="screen_gui">
- split_pgn allows you to split multiple games from a PGN file. The output PGNs will be saved in a folder specified by the user.
- INPUT ONE: pgn file (example: C:\users\u1\documents\matches.pgn)
- INPUT TWO: folder where the games will be saved (example: C:\users\u1\documents\folder_matches)
<img src="./images/screen_pgnmanager3.png" alt="screen_gui">


