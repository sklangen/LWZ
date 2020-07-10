from .utils import month_names, format_month_date
from .Mode import modes
from .SeasonDirectory import SeasonDirectory
from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader('lwz', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)



class SeasonDirectoryRenderer:
    def __init__(self, seasonDir: SeasonDirectory):
        self.seasonDir = seasonDir
        self.mode = modes[seasonDir.season.mode]
        self.headers = ['Name', 'DWZ', 'Attr', 'Punkte']

    @property
    def index(self):
        return env.get_template('player_ranking.html').render(
            title=self.mode.name + ' - ' + self.seasonDir.season.name,
            headers=self.headers,
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
                    format_month_date(self.seasonDir.as_date(m))
                ]),
                headers=self.headers,
                rows=self.tournament_ranking(t),
            )

    def tournament_ranking(self, tournament):
        for player in sorted(tournament.players, key=lambda p: p.rank):
            sp = next(filter(lambda p: p.id == player.id, self.seasonDir.season.players))
            yield sp.name, sp.dwz, self.mode.get_attr(sp), player.points

    @property
    def month_headers(self):
        for month in month_names:
            d = self.seasonDir.as_date(month)
            yield d.strftime('%Y_%m.html') if month in self.seasonDir.tournaments else None, format_month_date(d)

    @property
    def season_rows(self):
        for player, score, months in sorted(self.season_rows_calculated, key=lambda t: t[1], reverse=True):
            yield [player.name, player.dwz, self.mode.get_attr(player), score] + months

    @property
    def season_rows_calculated(self):
        for player in self.seasonDir.season.players:
            months_played = dict(self.seasonDir.months_played(player))

            if months_played:
                score = sum(sorted((p.points for p in months_played.values()), reverse=True)[:6])
                months = [getattr(months_played.get(m), 'points', '') for m in month_names]

                yield player, score, months
