from . import dewis
from .Mode import modes
from .Parser import parsers
from .SeasonDirectory import *
from .render import SeasonDirectoryRenderer, render_index
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
            sp = seasonDir.player_by_name(player.name)
            player.id = sp.id
            
        seasonDir.tournaments[parsed_month] = tournament
        seasonDir.dump_tournament(parsed_month)

    seasonDir.dump_season()


def build_html(directory, seasons):
    modes = {}

    for season in seasons:
        sd = SeasonDirectory(season)
        sd.load()

        path = Path(directory, sd.season.outdir)
        path.mkdir(parents=True, exist_ok=True)

        renderer = SeasonDirectoryRenderer(sd)
        modes.setdefault(renderer.mode, []).append(sd.season)

        try:
            (path/'index.html').write_text(renderer.index)
            for m, html in renderer.tournaments:
                (path/sd.as_date(m).strftime('%Y_%m.html')).write_text(html)
        except Exception:
            logging.exception('Building html for ' + season)
            raise

    (Path(directory)/'index.html').write_text(render_index(modes))
