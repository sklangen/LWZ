from . import dewis
from .Mode import modes
from .Parser import parsers
from .SeasonDirectory import *
from .render import SeasonDirectoryRenderer, render_index
from .utils import LWZException
from pathlib import Path
from tqdm import tqdm
import logging


def init_season(directory, mode, startYear, parentSeason=None):
    season = Season(mode, startYear, parentSeason=parentSeason)
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
            sp = seasonDir.get_player_by_name(player.name)
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
            logging.exception('Exception occurred whilst building html for ' + season)
            raise

    (Path(directory)/'index.html').write_text(render_index(modes))


def import_dsb(directory, zps=[], pkz=[], existing=False, members=False, progress=False):
    seasonDir = SeasonDirectory(directory)
    seasonDir.load_season()

    players = []

    for z in zps:
        players += list(dewis.get_club(z))

    for p in pkz:
        players.append(dewis.get_player(p))

    if existing:
        for p in seasonDir.season.players:
            if p.is_dsb:
                players.append(p)

    if progress:
        players = tqdm(players, desc='Getting data from dsb', ascii=True)

    for player in players:
        try:
            player.dwz = dewis.get_player_rating_at(player.id, seasonDir.season.startDate)
            logging.debug(f'Got data for: {player}')
        except Exception:
            logging.exception(f'Exception occurred whilst trying to get data for: {player}')

        if members:
            player.stateOfMembership = 'MEMBER'
        seasonDir.add_or_update_player(player)

    seasonDir.dump_season()
