# LWZ

CLI-Tool zum verwalten von vereinsinternen, monatlichen Turnieren.

## Todo

- [ ] Spieler- und Saisonklasse für `season.yml` untern Nutzung vom ![yaml.YAMLObject](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [ ] Mit Pip einen argparser in den `$PATH` ![installieren](https://docs.python.org/3/distutils/setupscript.html), der zumidest alle ![Subcommands](https://docs.python.org/dev/library/argparse.html) abfängt (Siehe Unten).
- [ ] Umsetzung des Befehls `lwz import --type old --startyear 2019 --mode BLITZ  -D blitz_5plus0_1920 ./resource/tournament/blitz_5plus0/season_2019` zum importieren der alten Daten.
- [ ] Tests, ob die Daten richtig importiert wurden und richtig eingelesen werden.
- [ ] Umsetzung des Befehls `lwz html -D public *` zum generieren der HTML-Tabellen.
- [ ] J.B. Tabellen zeigen (Sehr strenger Unit Test)

# Subocommands

Hier sind ein Paar beispielhafte Aufrufe, die es in Zukunft mal geben könnte:
```
lwz init # Anlegen einer neuen Saison im Arbeitsverzeichnis

lwz import --month jun --type lichess QLMFFLBq # Turnier von Lichess nach 2020_06.trf importieren. 

lwz html blitz_5plus0_* kids_* # HTML-Datein für alle Blitz- und Jugendturniere generieren.
```
