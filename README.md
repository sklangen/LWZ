# LWZ

CLI-Tool zum verwalten von vereinsinternen, monatlichen Turnieren.

## Todo

- [ ] Spieler- und Saisonklasse für `season.yml` unter Nutzung vom [yaml.YAMLObject](https://pyyaml.org/wiki/PyYAMLDocumentation#constructors-representers-resolvers).
  - [X] `Season (mode, startYear, [players], parentSeason)`
  - [X] `SeasonPlayer (playerId, [names], dwz, stateOfMembership)`
  - [X] Hilfsfunktion zum einlesen einer Saison mit gegebenem Ordnerpfad.
  - [X] Hilfsfunktion zum einlesen der Turniere im Ordner der `season.yml` unter Benutzung von <https://github.com/erral/fidetournament>.
  - [ ] Testen des Trf Parsers bis Ragnarök angebrochen ist.
  
- [X] Mit Pip einen Argparser in den `$PATH` [installieren](https://docs.python.org/3/distutils/setupscript.html#installing-scripts), der zumindest alle [Subcommands](https://docs.python.org/dev/library/argparse.html#sub-commands) kennt, sodass `lwz --help` gefüllt ist. Implementiert muss hier noch nichts sein.
  - [X] `lwz init` Anlegen einer Boilerplate `season.yml`.
  - [X] `lwz import` Importieren von Turnieren.
  - [X] `lwz html` Erstellen der HTML Tabellen.
  
- [ ] Umsetzung des Befehls `lwz import oldlwz` zum importieren der alten Daten.
  - [ ] Hilfsfunktion zum speichern einer Saison mit gegebenem Ordnerpfad.
  - [ ] Löschen von [Phantomturnieren](https://github.com/Tobias-Thomas/LWZ/commit/9f1a0c9f2616bdd31b2d6c606a1e2656a0c03d13#commitcomment-36659959).
  
- [ ] Tests, ob die Daten richtig importiert wurden und richtig eingelesen werden.

- [ ] Umsetzung des Befehls `lwz html` zum generieren der HTML-Tabellen. Hier kann hoffentlich einiges aus dem alten Projekt wiederverwendet werden.
  - [ ] Implementierung der Turnierordnung - Stichwort Moduslogik.
  - [ ] Schrieben von [Jinja2 Templates](https://palletsprojects.com/p/jinja/).

- [ ] J.B. Tabellen zeigen (Sehr strenger Unit Test ;).
