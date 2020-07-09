from . import dewis
from .Mode import modes
from .Parser import parsers
from .SeasonDirectory import *
from .render import SeasonDirectoryRenderer
from pathlib import Path
import logging


class LWZException(Exception):
    pass


def init_season(directory, mode, startYear, parentSeason=None, zps=None):
    season = Season(mode, startYear, parentSeason=parentSeason)

    if zps is not None:
        players = dewis.get_club(zps)
        season.players = sorted(players, key=lambda p: p.dwz)
    else:
        season.players.append(SeasonPlayer(1, names=['Oshgnacknak']))

    seasonDir = SeasonDirectory(directory, season=season)
    seasonDir.dump_season()


def import_tournaments(directory, tournaments, source, month=None, rounds=None):
    seasonDir = SeasonDirectory(directory)
    seasonDir.load_season()

    for tour in tournaments:
        tournament, parsed_month = parsers[source](tour)

        if rounds:
            tournament.xx_fields['XXR'] = rounds
        if month:
            parsed_month = month

        if not parsed_month in calendar.month_abbr[1:]:
            raise LWZException('Not a valid month: ' + month)
        tournament.xx_fields['XXM'] = parsed_month

        for player in tournament.players:
            candidates = list(filter(lambda p: player.name in p.aliases, seasonDir.season.players))

            if len(candidates) >= 2:
                raise LWZException('Too many name candidates: ' + str(candidates))
            elif not candidates:
                sp = seasonDir.add_player_by_name(player.name)
                logging.warn('Name not found, adding player: ' + repr(sp.name))
            else:
                sp = candidates[0]
            player.id = sp.id
            
        seasonDir.tournaments[parsed_month] = tournament
        seasonDir.dump_tournament(parsed_month)

    seasonDir.dump_season()


def build_html(directory, seasons):
    for season in seasons:
        sd = SeasonDirectory(season)
        sd.load()

        path = Path(Path(season).name)
        path.mkdir(parents=True, exist_ok=True)

        renderer = SeasonDirectoryRenderer(sd)
        (path/'index.html').write_text(renderer.index)

        for m, html in renderer.tournaments:
            (path/sd.as_date(m).strftime('%Y_%m.html')).write_text(html)
