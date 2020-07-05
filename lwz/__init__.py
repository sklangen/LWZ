from .SeasonDirectory import *
from . import dewis

def init_season(directory, mode, startYear, parentSeason=None, zps=None):
    season = Season(mode, startYear, parentSeason=parentSeason)

    if zps is not None:
        players = dewis.get_club(zps)
        season.players = sorted(players, key=lambda p: p.dwz)

    sd = SeasonDirectory(directory, season=season)
    sd.dump_season()

def import_tournament(directory, tournament, source, month, rounds=None):
    logging.warn('Not gonna import!')

def build_html(directory, seasons):
    logging.warn('Not gonna build!')
