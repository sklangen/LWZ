from .utils import month_names, format_month_date
from .Mode import modes
from .SeasonDirectory import SeasonDirectory
from jinja2 import Environment, PackageLoader, select_autoescape
import logging


env = Environment(
    loader=PackageLoader('lwz', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def render_index(modes) -> str:
    return env.get_template('index.html').render(
        title='Alle Saisons aller Modi',
        modes=modes
    )


class SeasonDirectoryRenderer:
    def __init__(self, seasonDir: SeasonDirectory):
        self.seasonDir = seasonDir
        self.mode = modes[seasonDir.season.mode]
        self.headers = ['Platz', 'Name', 'DWZ', 'Attr']

    @property
    def index(self):
        return env.get_template('player_ranking.html').render(
            title=self.mode.name + ' - ' + self.seasonDir.season.name,
            headers=self.headers + [self.mode.score_header],
            month_headers=list(self.month_headers),
            rows=self.season_rows,
        )

    @property
    def tournaments(self):
        for m, t in self.seasonDir.tournaments.items():
            yield m, env.get_template('player_ranking.html').render(
                title=' - '.join([
                    self.mode.name,
                    self.seasonDir.season.name,
                    format_month_date(self.seasonDir.as_date(m)) + ' oiawjd',
                    f'{t.numrounds} Runden'
                ]),
                headers=self.headers + ['Punkte'],
                rows=self.tournament_ranking(t),
            )

    def tournament_ranking(self, tournament):
        rows = sorted(tournament.players, key=lambda p: p.rank)
        for i, player in enumerate(rows):
            try:
                sp = next(filter(lambda p: p.id == player.id, self.seasonDir.all_players))
                yield [i+1, sp.name, sp.dwz, self.mode.get_attr(sp), player.points]
            except StopIteration:
                logging.exception('No SeasonPlayer for: ' + str(player))
                raise

    @property
    def month_headers(self):
        for month in month_names:
            d = self.seasonDir.as_date(month)
            yield d.strftime('%Y_%m.html') if month in self.seasonDir.tournaments else None, format_month_date(d)

    @property
    def season_rows(self):
        season_results = sorted(self.season_results_calculated, key=lambda t: t[1], reverse=True)
        for i, (player, score, months) in enumerate(season_results):
            yield [i+1, player.name, player.dwz, self.mode.get_attr(player), self.mode.format_score(score)] + months

    @property
    def season_results_calculated(self):
        for player in self.seasonDir.all_players:
            months_played = dict(self.seasonDir.months_played(player))

            if months_played:
                score = sum(sorted((self.mode.get_score(p, t) for p, t in months_played.values()), reverse=True)[:6])
                months = [
                    months_played[m][0].points
                    if m in months_played else ''
                    for m in month_names]

                yield player, score, months
