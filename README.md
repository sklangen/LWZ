# LWZ

CLI-Tool zum verwalten von vereinsinternen, monatlichen Turnieren.

## Todo

- [ ] Spieler- und Saisonklasse für `season.yml` untern Nutzung vom [yaml.YAMLObject](https://pyyaml.org/wiki/PyYAMLDocumentation#constructors-representers-resolvers).
  - [ ] `Season (mode, startYear, [players], parentSeason)`
  - [ ] `SeasonPlayer (playerId, name, dwz, stateOfMembership)`
  - [ ] Hilfsfunktion zum einlesen einer Saison mit gegebenem Ordnerpfad.
  
- [ ] Mit Pip einen argparser in den `$PATH` [installieren](https://docs.python.org/3/distutils/setupscript.html#installing-scripts), der zumidest alle [Subcommands](https://docs.python.org/dev/library/argparse.html#sub-commands) kennt, sodass `lwz --help` gefüllt ist. Implementiert muss hier noch nichts sein.
  - [ ] `lwz init` Anlegen einer Boilerplate `season.yml`.
  - [ ] `lwz import` Importieren von Turnieren.
  - [ ] `lwz html` Erstellen der HTML Tabellen.
  
- [ ] Umsetzung des Befehls `lwz import oldlwz` zum importieren der alten Daten.
  - [ ] Hilfsfunktion zum speichern einer Saison mit gegebenem Ordnerpfad.
  - [ ] Löschen von [Phantomturnieren](https://github.com/Tobias-Thomas/LWZ/commit/9f1a0c9f2616bdd31b2d6c606a1e2656a0c03d13#commitcomment-36659959).
  
- [ ] Tests, ob die Daten richtig importiert wurden und richtig eingelesen werden.

- [ ] Umsetzung des Befehls `lwz html` zum generieren der HTML-Tabellen. Hier kann hoffentlich einiges aus dem alten Projekt wiederverwendet werden.
  - [ ] Implementierung der Turnierordnung - Stichwort Moduslogik.
  - [ ] Schrieben von [Jinja2 Templates](https://palletsprojects.com/p/jinja/).

- [ ] J.B. Tabellen zeigen (Sehr strenger Unit Test ;).
