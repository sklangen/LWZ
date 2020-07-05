from . import dewis
from .Parser import parsers
from .SeasonDirectory import *
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
        parsed = parsers[source](tour)

        tournament = parsed['tournament']
        tournament.xx_fields['XXR'] = rounds or parsed.get('rounds', max(len(p.rounds) for p in tournament.players))

        parsed_month = month or parsed['month']
        if not parsed_month in calendar.month_abbr[1:]:
            raise LWZException('No a valid month: ' + month)

        for player in tournament.players:
            candidates = list(filter(lambda p: player.name in p.names, seasonDir.season.players))

            if len(candidates) >= 2:
                raise LWZException('Too many name candidates: ' + str(candidates))
            elif not candidates:
                sp = SeasonPlayer(
                    id=max((p.id for p in seasonDir.season.players if p.id < 10_000_000), default=0)+1,
                    stateOfMembership='GUEST',
                    names=[player.name]
                )

                seasonDir.season.players.append(sp)
                logging.warn('Name not found adding player: ' + str(sp))
            else:
                sp = candidates[0]
            player.id = sp.id
            
        print(parsed_month)
        seasonDir.tournaments[parsed_month] = tournament
    seasonDir.dump()


def build_html(directory, seasons):
    logging.warn('Not gonna build!')
